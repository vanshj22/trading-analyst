import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "blocks.mvp-subha.me",
        pathname: "/assets/**",
      },
    ],
  },
};

export default nextConfig;
