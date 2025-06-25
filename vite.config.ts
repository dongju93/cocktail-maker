import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import react from '@vitejs/plugin-react'


// https://vite.dev/config/
export default defineConfig({
	plugins: [react(), tailwindcss()],
	server: {
		port: 3000,
		// 개발 서버에서 API 프록시 설정 (선택사항)
		proxy: {
			"/api": {
				target: "http://localhost:8000", // 백엔드 서버 주소
				changeOrigin: true,
			},
		},
	},
	build: {
		outDir: "dist",
		sourcemap: true,
	},
});
