# Gradle Setup

## Full build.gradle

```groovy
plugins {
    id 'java'
    id 'application'
}

group = 'com.example'
version = '1.0.0'

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

application {
    mainClass = 'com.example.CrawlApp'
}

repositories {
    mavenCentral()
}

dependencies {
    // === Anthropic ===
    implementation 'com.anthropic:anthropic-java:2.5.0'

    // === MCP SDK (maintained with Spring AI) ===
    implementation 'io.modelcontextprotocol:java-sdk:0.9.0'

    // === Web Crawling ===
    implementation 'edu.uci:crawler4j:4.4.0'
    implementation 'org.jsoup:jsoup:1.17.2'

    // === Bloom Filters ===
    implementation 'com.google.guava:guava:33.4.0-jre'

    // === LangChain4j (prompt templates, RAG) ===
    implementation 'dev.langchain4j:langchain4j:1.0.0'
    implementation 'dev.langchain4j:langchain4j-anthropic:1.0.0'

    // === LSP ===
    implementation 'org.eclipse.lsp4j:org.eclipse.lsp4j:0.23.1'

    // === Data Processing ===
    implementation 'com.fasterxml.jackson.core:jackson-databind:2.17.0'
    implementation 'com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.17.0'

    // === Local Storage ===
    implementation 'org.xerial:sqlite-jdbc:3.45.0.0'

    // === Logging ===
    implementation 'org.slf4j:slf4j-api:2.0.12'
    runtimeOnly 'ch.qos.logback:logback-classic:1.5.3'

    // === Testing ===
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

test {
    useJUnitPlatform()
}

// Fat jar for deployment
tasks.register('fatJar', Jar) {
    archiveClassifier = 'all'
    from { configurations.runtimeClasspath.collect { it.isDirectory() ? it : zipTree(it) } }
    with jar
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    manifest {
        attributes 'Main-Class': application.mainClass
    }
}
```

## Gradle Kotlin DSL (build.gradle.kts)

```kotlin
plugins {
    java
    application
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

application {
    mainClass.set("com.example.CrawlApp")
}

dependencies {
    implementation("com.anthropic:anthropic-java:2.5.0")
    implementation("edu.uci:crawler4j:4.4.0")
    implementation("org.jsoup:jsoup:1.17.2")
    implementation("com.google.guava:guava:33.4.0-jre")
    implementation("dev.langchain4j:langchain4j:1.0.0")
    implementation("dev.langchain4j:langchain4j-anthropic:1.0.0")
    implementation("org.eclipse.lsp4j:org.eclipse.lsp4j:0.23.1")
}
```

## Directory Structure

```
crawl-project/
├── build.gradle
├── settings.gradle
├── src/
│   ├── main/
│   │   ├── java/com/example/
│   │   │   ├── CrawlApp.java          # Entry point
│   │   │   ├── crawler/
│   │   │   │   ├── ProductCrawler.java # WebCrawler implementation
│   │   │   │   └── BloomDedup.java     # Bloom filter wrapper
│   │   │   ├── extract/
│   │   │   │   ├── ClaudeExtractor.java # Anthropic SDK integration
│   │   │   │   └── JsoupParser.java     # HTML parsing
│   │   │   └── storage/
│   │   │       ├── SqliteStore.java     # Local SQLite storage
│   │   │       └── CrawlRecord.java    # Data model
│   │   └── resources/
│   │       └── logback.xml
│   └── test/
│       └── java/com/example/
│           └── CrawlerTest.java
└── data/                               # Runtime data directory
    ├── crawl/                          # crawler4j storage
    ├── bloom.bin                       # Serialized bloom filter
    └── crawl.db                        # SQLite database
```
