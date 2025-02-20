module.exports = {
    root: true,
    env: {
      node: true
    },
    extends: [
      'plugin:vue/essential',
      'eslint:recommended'
    ],
    parserOptions: {
      parser: 'babel-eslint'
    },
    rules: {
      'vue/no-unused-components': 'off',  // 禁用未使用组件规则
      "vue/no-v-model-argument": "off",
      "no-unused-vars": "off"
    }
  };
  