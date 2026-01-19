import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "THC Meal Prep Planner",
  description: "Your weekly meal planning and grocery list companion",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
