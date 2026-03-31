plugins {
    scala
    application
}

repositories {
    mavenCentral()
}

dependencies {
    // Netflix Atlas chart rendering (Scala 2.13)
    implementation("com.netflix.atlas_v1:atlas-chart_2.13:1.7.0-rc.22")

    // Postgres JDBC for reading from Neon
    implementation("org.postgresql:postgresql:42.7.4")

    // Scala standard library
    implementation("org.scala-lang:scala-library:2.13.15")
}

application {
    mainClass.set("agentstreams.AtlasChartRenderer")
}

// Use system Java (25+)
tasks.withType<ScalaCompile>().configureEach {
    scalaCompileOptions.additionalParameters = listOf("-release", "17")
}
