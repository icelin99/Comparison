<template>
    <div class="markdown-editor">
      <div class="markdown-editor-container">
        <textarea v-model="input" placeholder="Enter Markdown text here..."></textarea>
        <div v-html="compiledMarkdown" class="preview" ></div>
      </div>
      <div class="markdown-editor-container">
        <textarea v-model="formula" placeholder="Enter Latex formula here..."></textarea>
        <div v-html="compiledLatex" class="preview" ></div>
      </div>
    </div>
</template>
  
<script>
import MarkdownIt from 'markdown-it';
import markdownItTable from 'markdown-it-multimd-table';
import markdownItContainer from 'markdown-it-container';
import 'katex/dist/katex.min.css';
import Katex from 'katex';
// import MathJax from 'mathjax';
import CodeBlockRenderer from '../components/CodeBlockRenderer.vue'
import markdownItKatex from "markdown-it-katex";
  
export default {
    components: {
      CodeBlockRenderer
    },
    data() {
      return {
        input: '',
        formula: "",
        markdownItInstance: null
      };
    },
    created() {
      this.markdownItInstance = new MarkdownIt({
        html: true, // 允许 HTML 标签
        breaks: true, // 将 \n 转换为 <br>
        linkify: true, // 自动将 URL 转为链接
      })
      .use(markdownItTable)
      .use(markdownItContainer)
      .use(markdownItKatex)
      // .use(this.katexPlugin)

      
    },
    computed: {
      compiledMarkdown() {
        // 初始化 markdown-it 并使用 markdown-it-container 插件
        const sanitizedInput = this.input.replace(/\\n/g, '\n').trim();
        let renderMark = this.markdownItInstance.render(sanitizedInput);
        return renderMark;
      },
      compiledLatex() {
        return Katex.renderToString(this.formula, {
          throwOnError: false,
          displayMode: true
        });
      }
    },
    methods: {
      renderLatex(content) {
        const regex = /\$\$(.*?)\$\$/g; // 正则表达式匹配块级公式
        const inlineRegex = /\\\((.*?)\\\)/g; // 正则表达式匹配内联公式

        // 处理块级公式
        content = content.replace(regex, (match, p1) => {
          try {
            return Katex.renderToString(p1, { displayMode: true });
          } catch (err) {
            return `<span style="color: red;">${err.message}</span>`;
          }
        });

        // 处理内联公式
        content = content.replace(inlineRegex, (match, p1) => {
          try {
            return Katex.renderToString(p1, { displayMode: false });
          } catch (err) {
            return `<span style="color: red;">${err.message}</span>`;
          }
        });
        console.log("render latex",content)
        console.log("render latex2",Katex.renderToString(content, { displayMode: false }));
        return content;
      },
    },
};
</script>
  
<style scoped>
.markdown-editor {
    display: flex;
    gap: 20px;
    flex-direction: column;
}
.markdown-editor-container {
  display: flex;
}
textarea {
    width: 50%;
    height: 300px;
}
  
.preview {
    width: 50%;
    border: 1px solid #ddd;
    padding: 10px;
    background-color: #f9f9f9;
    overflow: auto;
}
  </style>
  