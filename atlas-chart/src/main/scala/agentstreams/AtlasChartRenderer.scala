package agentstreams

import java.awt.Color
import java.io.FileOutputStream
import java.sql.{DriverManager, ResultSet}
import java.time.Instant
import scala.collection.mutable

import com.netflix.atlas.chart.DefaultGraphEngine
import com.netflix.atlas.chart.model.{GraphDef, LegendType, LineDef, PlotDef}
import com.netflix.atlas.core.model.{ArrayTimeSeq, DsType, TimeSeries}

/** Reads metric_values from Neon Postgres and renders Atlas PNG charts.
  *
  * Atlas data model mapping:
  *   metric_values.recorded_at → ArrayTimeSeq timestamps
  *   metric_values.value       → ArrayTimeSeq data array
  *   metric_values.tags (JSONB)→ TimeSeries tag map
  *   metrics.type              → DsType (gauge vs rate)
  */
object AtlasChartRenderer {

  // Chart palette — distinct colors for multi-series plots
  val PALETTE: Array[Color] = Array(
    new Color(0x1f77b4), // blue
    new Color(0xff7f0e), // orange
    new Color(0x2ca02c), // green
    new Color(0xd62728), // red
    new Color(0x9467bd), // purple
    new Color(0x8c564b), // brown
    new Color(0xe377c2), // pink
    new Color(0x7f7f7f), // gray
    new Color(0xbcbd22), // yellow-green
    new Color(0x17becf)  // cyan
  )

  // Metric type → Atlas DsType
  def toDsType(metricType: String): DsType = metricType match {
    case "counter"              => DsType.Rate
    case "timer"                => DsType.Rate
    case "distribution_summary" => DsType.Rate
    case "gauge"                => DsType.Gauge
    case _                      => DsType.Gauge
  }

  // Metric configs: name → (title, unit, y-label)
  val METRIC_CONFIGS: Map[String, (String, String)] = Map(
    "agentstreams.pipeline.duration" -> ("Pipeline Stage Duration", "seconds"),
    "agentstreams.api.requests"      -> ("Claude API Requests (rate/min)", "req/min"),
    "agentstreams.api.tokens"        -> ("Token Usage (rate/min)", "tokens/min"),
    "agentstreams.api.cost"          -> ("API Cost per Request", "USD"),
    "agentstreams.eval.score"        -> ("Eval Pass Rate", "ratio"),
    "agentstreams.crawl.pages"       -> ("Pages Crawled (rate/min)", "pages/min"),
    "agentstreams.crawl.dedup"       -> ("Bloom Filter False Positive Rate", "ratio")
  )

  case class SeriesData(
    metricName: String,
    tags: Map[String, String],
    timestamps: Array[Long],  // epoch millis
    values: Array[Double]
  )

  def main(args: Array[String]): Unit = {
    val jdbcUrl = sys.env.getOrElse("NEON_JDBC_URL",
      sys.error("NEON_JDBC_URL environment variable is required. " +
        "Format: jdbc:postgresql://host/db?user=...&password=...&sslmode=require")
    )
    val outputDir = if (args.length > 0) args(0) else "charts"

    new java.io.File(outputDir).mkdirs()

    println(s"Connecting to Neon...")
    val conn = DriverManager.getConnection(jdbcUrl)

    try {
      // Get metric types
      val metricTypes = mutable.Map[String, String]()
      val typeStmt = conn.createStatement()
      val typeRs = typeStmt.executeQuery("SELECT name, type FROM metrics")
      while (typeRs.next()) {
        metricTypes(typeRs.getString("name")) = typeRs.getString("type")
      }
      typeRs.close()
      typeStmt.close()

      // For each metric, fetch all series and render a chart
      for (metricName <- METRIC_CONFIGS.keys.toSeq.sorted) {
        val (title, ylabel) = METRIC_CONFIGS(metricName)
        val dsType = toDsType(metricTypes.getOrElse(metricName, "gauge"))

        println(s"Fetching data for $metricName...")
        val series = fetchSeries(conn, metricName)

        if (series.nonEmpty) {
          println(s"  ${series.size} series, ${series.head.values.length} points each")
          val outPath = s"$outputDir/${metricName.replace('.', '-')}.png"
          renderChart(series, dsType, title, ylabel, outPath)
          println(s"  → $outPath")
        } else {
          println(s"  No data found, skipping")
        }
      }
    } finally {
      conn.close()
    }

    println("Done.")
  }

  def fetchSeries(conn: java.sql.Connection, metricName: String): Seq[SeriesData] = {
    // Get distinct tag combinations for this metric
    val tagStmt = conn.prepareStatement(
      """SELECT DISTINCT tags::text as tags_text
        |FROM metric_values
        |WHERE metric_name = ?
        |ORDER BY tags_text""".stripMargin
    )
    tagStmt.setString(1, metricName)
    val tagRs = tagStmt.executeQuery()

    val tagSets = mutable.ArrayBuffer[String]()
    while (tagRs.next()) {
      tagSets += tagRs.getString("tags_text")
    }
    tagRs.close()
    tagStmt.close()

    // For each tag combination, fetch time-ordered values
    val dataStmt = conn.prepareStatement(
      """SELECT recorded_at, value
        |FROM metric_values
        |WHERE metric_name = ? AND tags::text = ?
        |ORDER BY recorded_at""".stripMargin
    )

    tagSets.map { tagsJson =>
      dataStmt.setString(1, metricName)
      dataStmt.setString(2, tagsJson)
      val rs = dataStmt.executeQuery()

      val timestamps = mutable.ArrayBuffer[Long]()
      val values = mutable.ArrayBuffer[Double]()
      while (rs.next()) {
        timestamps += rs.getTimestamp("recorded_at").toInstant.toEpochMilli
        values += rs.getDouble("value")
      }
      rs.close()

      // Parse JSONB tags
      val tags = parseJsonTags(tagsJson)

      SeriesData(metricName, tags, timestamps.toArray, values.toArray)
    }.toSeq
  }

  def parseJsonTags(json: String): Map[String, String] = {
    // Simple JSON object parser for {"key": "value", ...}
    val entries = json.trim.stripPrefix("{").stripSuffix("}")
    if (entries.trim.isEmpty) return Map.empty

    entries.split(",").map { entry =>
      val parts = entry.split(":", 2)
      val key = parts(0).trim.stripPrefix("\"").stripSuffix("\"")
      val value = parts(1).trim.stripPrefix("\"").stripSuffix("\"")
      key -> value
    }.toMap
  }

  def renderChart(
    series: Seq[SeriesData],
    dsType: DsType,
    title: String,
    ylabel: String,
    outputPath: String
  ): Unit = {
    // All series share the same time range and step
    val first = series.head
    val startMillis = first.timestamps.head
    val stepMillis = if (first.timestamps.length > 1) {
      first.timestamps(1) - first.timestamps(0)
    } else {
      300000L // default 5 min
    }
    val endMillis = first.timestamps.last + stepMillis

    // Build Atlas TimeSeries for each series
    val lines = series.zipWithIndex.map { case (sd, idx) =>
      val seq = new ArrayTimeSeq(dsType, startMillis, stepMillis, sd.values)

      // Label from tags
      val label = sd.tags.map { case (k, v) => s"$k=$v" }.mkString(", ")
      val tags = sd.tags + ("name" -> sd.metricName)

      val ts = TimeSeries(tags, label, seq)
      val color = PALETTE(idx % PALETTE.length)

      LineDef(data = ts, color = color, lineWidth = 1.5f)
    }

    val plot = PlotDef(
      data = lines.toList,
      ylabel = Some(ylabel)
    )

    val graphDef = GraphDef(
      plots = List(plot),
      startTime = Instant.ofEpochMilli(startMillis),
      endTime = Instant.ofEpochMilli(endMillis),
      step = stepMillis,
      width = 900,
      height = 350,
      title = Some(title),
      legendType = LegendType.LABELS_WITH_STATS
    )

    val engine = new DefaultGraphEngine
    val fos = new FileOutputStream(outputPath)
    try {
      engine.write(graphDef, fos)
    } finally {
      fos.close()
    }
  }
}
