import type { Metadata, Viewport } from "next";
import { Outfit, Crimson_Pro, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
});

const crimsonPro = Crimson_Pro({
  subsets: ["latin"],
  variable: "--font-crimson",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://agentcrawls.com"),
  title: "agentstreams — Multi-Agent Orchestration",
  description:
    "Safety-grounded AI agent orchestration with Mythos-grade methodology. " +
    "Composable pipelines across codegen, security audit, alignment audit, and eval.",
  openGraph: {
    title: "agentstreams — Multi-Agent Orchestration",
    description:
      "Safety-grounded AI agent orchestration with Mythos-grade methodology. " +
      "Composable pipelines across codegen, security audit, alignment audit, and eval.",
    url: "https://agentcrawls.com",
    siteName: "agentstreams",
    type: "website",
  },
  twitter: {
    card: "summary",
    title: "agentstreams — Multi-Agent Orchestration",
    description:
      "Safety-grounded AI agent orchestration with Mythos-grade methodology.",
  },
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
    <html
      lang="en"
      className={`h-full ${outfit.variable} ${crimsonPro.variable} ${jetbrainsMono.variable}`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
