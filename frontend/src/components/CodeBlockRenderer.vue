<template>
    <div v-html="renderedContent"></div>
  </template>
  
  <script>
  import hljs from 'highlight.js';
  import 'highlight.js/styles/default.css';
  import { marked } from 'marked';
  import katex from 'katex';
    import 'katex/dist/katex.min.css';

  
  export default {
    // props: {
    //   content: {
    //     type: String,
    //     required: true
    //   }
    // },
    data() {
      return {
        renderedContent: '',
        content:  "Certainly, I'll identify the formula in the image and convert it to LaTeX format for you.\n```latex\n\\begin{equation*}\nx'(t)=\\begin{pmatrix} 0 & -1 & 0 & 0 \\\\ 0 & 0 & 0 & 1 \\end{pmatrix} x(t)\n\\end{equation*}\n```"
      };
    },
    watch: {
      content: 'renderContent'
    },
    mounted() {
      this.renderContent();
    },
    methods: {
      renderContent() {
        let content = this.content;
        
        console.log("=====",content)
        // 处理代码块
        content = content.replace(/```([\s\S]*?)\n([\s\S]*?)```/g, function(match, lang, code) {
            console.log("Matched language:", lang, code);
            if (lang.trim() === 'latex') {
                try {
                    return katex.renderToString(code, { displayMode: true });
                } catch (error) {
                    return `<pre><code class="language-latex">${code}</code></pre>`; // 如果解析失败，返回原始字符串
                }
            } else {
                return `<pre><code class="language-${lang.trim()}">${code}</code></pre>`;
            }
        });
        content = content.replace(/\\n/g, '\n').replace(/^```markdown/, '').replace(/```$/, '').replace(/```/g, '\\`\\`\\`');
        // 处理行内公式
        content = content.replace(/\$([^$]+)\$/g, function(match, p1) {
          return `\\(${p1}\\)`;
        });
  
        // 处理块级公式
        content = content.replace(/\$\$([\s\S]*?)\$\$/g, function(match, p1) {
          return `\\[${p1}\\]`;
        });
        
         // 处理 LaTeX 公式
         function replaceLatex(match, p1) {
            console.log("处理latex公式：",p1);
            try {
                return katex.renderToString(p1, { displayMode: false });
            } catch (error) {
                return match; // 如果解析失败，返回原始字符串
            }
        }

        function replaceBlockLatex(match, p1) {
            console.log("处理latex复杂公式：",p1);
            try {
                return katex.renderToString(p1, { displayMode: true });
            } catch (error) {
                return match; // 如果解析失败，返回原始字符串
            }
        }
        // 处理行内公式
        content = content.replace(/\$([^$]+)\$/g, replaceLatex);

        // 处理块级公式
        content = content.replace(/\$\$([\s\S]*?)\$\$/g, replaceBlockLatex);

        // 处理复杂的 LaTeX 公式
        content = content.replace(/\\begin{([\s\S]*?)}([\s\S]*?)\\end{([\s\S]*?)}/g, function(match, p1, p2, p3) {
            if (p1 === p3) {
                try {
                    return katex.renderToString(`\\begin{${p1}}${p2}\\end{${p3}}`, { displayMode: true });
                } catch (error) {
                    return match; // 如果解析失败，返回原始字符串
                }
            }
            return match; // 如果不匹配，返回原始字符串
        });
        // 处理Markdown
        this.renderedContent = marked(content);
  
        this.$nextTick(() => {
          // 语法高亮
          this.$el.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
          });
  
          // 渲染LaTeX公式
          if (window.MathJax) {
            window.MathJax.typesetPromise();
          }
          
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* 你可以在这里添加一些样式 */
  </style>
  