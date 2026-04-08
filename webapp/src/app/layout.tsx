import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "agentstreams — Multi-Agent Orchestration",
  description:
    "Safety-grounded AI agent orchestration with Mythos-grade methodology. " +
    "Composable pipelines across codegen, security audit, alignment audit, and eval.",
};

export const viewport: Viewport = {
  themeColor: "#050505",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
