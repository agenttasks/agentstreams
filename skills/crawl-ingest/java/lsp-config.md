# Java LSP Configuration

## LSP4J Setup

LSP4J provides Java bindings for the Language Server Protocol.

### Maven/Gradle

```groovy
implementation 'org.eclipse.lsp4j:org.eclipse.lsp4j:0.23.1'
```

### Programmatic Client

```java
import org.eclipse.lsp4j.*;
import org.eclipse.lsp4j.launch.LSPLauncher;
import org.eclipse.lsp4j.services.LanguageServer;

import java.io.*;

public class LspClient {
    public static void main(String[] args) throws Exception {
        // Launch Eclipse JDT LS as subprocess
        ProcessBuilder pb = new ProcessBuilder(
            "jdtls",  // Eclipse JDT Language Server
            "--stdio"
        );
        Process process = pb.start();

        // Create LSP launcher
        var launcher = LSPLauncher.createClientLauncher(
            new MyLanguageClient(),
            process.getInputStream(),
            process.getOutputStream()
        );

        LanguageServer server = launcher.getRemoteProxy();
        launcher.startListening();

        // Initialize
        InitializeParams initParams = new InitializeParams();
        initParams.setRootUri("file:///path/to/project");
        initParams.setCapabilities(new ClientCapabilities());

        var initResult = server.initialize(initParams).get();
        server.initialized(new InitializedParams());

        // Request completions
        CompletionParams completionParams = new CompletionParams();
        completionParams.setTextDocument(
            new TextDocumentIdentifier("file:///path/to/File.java")
        );
        completionParams.setPosition(new Position(10, 15));

        var completions = server.getTextDocumentService()
            .completion(completionParams).get();
    }
}

class MyLanguageClient implements org.eclipse.lsp4j.services.LanguageClient {
    @Override
    public void publishDiagnostics(PublishDiagnosticsParams params) {
        params.getDiagnostics().forEach(d ->
            System.out.println(d.getSeverity() + ": " + d.getMessage())
        );
    }
    // ... other callbacks
}
```

## Eclipse JDT Language Server

Install via:
```bash
# macOS (Homebrew)
brew install jdtls

# Or download from Eclipse
# https://download.eclipse.org/jdtls/
```

## Key LSP Capabilities for Java Crawl Projects

| Feature | Method | Use Case |
|---------|--------|----------|
| Completions | `textDocument/completion` | Anthropic SDK, Guava, JSoup API discovery |
| Diagnostics | `textDocument/publishDiagnostics` | Compile errors, type mismatches |
| Go to definition | `textDocument/definition` | Navigate crawler/extractor code |
| Find references | `textDocument/references` | Track BloomFilter usage across classes |
| Rename | `textDocument/rename` | Refactor extraction fields |
