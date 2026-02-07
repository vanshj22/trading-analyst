import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AppProvider } from "@/lib/context";
import { Header } from "@/components/ui/header";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Antifragile Mirror | AI-Powered Trading Analyst",
  description:
    "AI-Powered Trading Analyst + Behavioral Coach + Social Content Engine. Built with Gemini 2.0 Flash.",
  keywords: ["trading", "AI", "behavioral", "analysis", "crypto", "stocks"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <AppProvider>
          <Header />
          <main className="min-h-screen">{children}</main>
          <footer className="border-t border-white/[0.06] py-8 text-center">
            <div className="container mx-auto px-6">
              <p className="text-sm text-white/40">
                Antifragile Mirror v2.0
              </p>
            </div>
          </footer>
        </AppProvider>
      </body>
    </html>
  );
}
