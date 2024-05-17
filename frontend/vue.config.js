const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  outputDir: "/var/www/html/mllm_evaluation",
  transpileDependencies: true,
  devServer: {
    port: 8082
  }
})
