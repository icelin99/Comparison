<template>
    <div class="markdown-editor">
      <div class="markdown-editor-container">
        <textarea v-model="input" placeholder="Enter Markdown text here..."></textarea>
        <div v-html="renderMarkdown(input)" class="preview" ></div>
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
import markdownItKatex from "markdown-it-katex";
import showdown from 'showdown';
import showdownKatex from 'showdown-katex';
// import { marked } from 'marked';
import hljs from 'highlight.js';
  import 'highlight.js/styles/default.css';

// import showdown from 'showdown';
// import showdownKatex from 'showdown-katex';
  
export default {
    components: {
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
        // let renderMark = //this.markdownItInstance.render(sanitizedInput);
        // this.renderLatex(sanitizedInput);
        const renderMark = this.transformInput(sanitizedInput);
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
      transformInput(input) {
        input = input.replace("<br />","\n").replace("<br/>","\n");
        let converter = new showdown.Converter({
          tables: true,
          strikethrough: true,
          underline: true,
          extensions: [
            showdownKatex({
              throwOnError: false,
              displayMode: false,
              delimiters: [
                { left: "$$", right: "$$", display: false },
                { left: "$", right: "$", display: false },
                { left: "~", right: "~", display: false, asciimath: true },
              ]
            })
          ]
        });
        return converter.makeHtml(input);
      },
      renderMarkdown(content) {
        console.log("0000",content)
            // 处理代码块
            content = content.replace(/```([\s\S]*?)\n([\s\S]*?)```/g, function(match, lang, code) {
                console.log("Matched language:", lang, code);
                if (lang.trim() === 'latex' || lang.trim() === 'asciimath') {
                    try {
                        return Katex.renderToString(code, { displayMode: true });
                    } catch (error) {
                        return `<pre><code class="language-latex">${code}</code></pre>`; // 如果解析失败，返回原始字符串
                    }
                } else {
                    return `<pre><code class="language-${lang.trim()}">${code}</code></pre>`;
                }
            });
            content = content.replace(/\\n/g, '\n').replace(/^```markdown/, '').replace(/```$/, '').replace(/```/g, '\\`\\`\\`');

            // 先渲染markdown
            let converter = new showdown.Converter({
            tables: true,
            strikethrough: true,
            underline: true,
            extensions: [
              showdownKatex({
                throwOnError: false,
                displayMode: false,
                delimiters: [
                  { left: "$$", right: "$$", display: false },
                  { left: "$", right: "$", display: false },
                  { left: "~", right: "~", display: false, asciimath: true },
                ]
              })
            ]
          });

            // 处理行内公式
            // convertedContent = convertedContent.replace(/\$([^$]+)\$/g, function(match, p1) {
            // return `\\(${p1}\\)`;
            // });
            //convertedContent = convertedContent.replace(/\\(?![\\])/g, '\\\\');

            // 处理块级公式
            // convertedContent = convertedContent.replace(/\$\$([\s\S]*?)\$\$/g, function(match, p1) {
            //     return `\\[${p1}\\]`;
            // });
            // 处理 LaTeX 公式
            function replaceInlineLatex(match, p1) {
                console.log("处理latex公式：",p1);
                try {
                    return Katex.renderToString(p1, { displayMode: false });
                } catch (error) {
                    return match; // 如果解析失败，返回原始字符串
                }
            }

            function replaceBlockLatex(match, p1) {
                console.log("处理latex复杂公式：",p1);
                try {
                    return Katex.renderToString(p1, { displayMode: true });
                } catch (error) {
                    return match; // 如果解析失败，返回原始字符串
                }
            }
            
            // 处理复杂的 LaTeX 公式
            function replaceEnvironment(match,slashes, p1, p2) {
                console.log("处理LaTeX环境公式：",p1, `${slashes}begin{${p1}}${p2}${slashes}end{${p1}}`);
                const environments = ['align', 'align*', 'equation', 'equation*', 'flalign','flalign*','gather', 'gather*', 'multline', 'multline*','subequations','subequations*','split','split*','gathered','gathered*','aligned','aligned*','alignedat','alignedat*'];
                console.log(environments.includes(p1),environments.includes("align*"))
                if (environments.includes(p1)) {
                  console.log("yyyyy")
                    try {
                      console.log("nnnnn")
                      console.log(`\\begin{${p1}}${p2}\\end{${p1}}`)
                        return Katex.renderToString(`\\begin{${p1}}${p2}\\end{${p1}}`, { displayMode: true });
                    } catch (error) {
                      console.log("error katex",error)
                        return match; // 如果解析失败，返回原始字符串
                    }
                }
                return match; // 如果不匹配，返回原始字符串
            }
            // // 处理行内公式
            // convertedContent = convertedContent.replace(/\$([^$]+)\$/g, replaceLatex);

            // // 处理块级公式
            // convertedContent = convertedContent.replace(/\$\$([\s\S]*?)\$\$/g, replaceBlockLatex);

            // // 处理复杂的 LaTeX 公式环境
            // convertedContent = convertedContent.replace(/(\\{1,2})begin{(\w+[*]?)}([\s\S]*?)\1end{\2}/g, replaceEnvironment);

            // 占位符存储
            let latexPlaceholders = [];

            // 替换所有LaTeX公式为占位符
            let processedContent = content
                .replace(/\$\$([\s\S]*?)\$\$/g, (match, p1) => {
                  latexPlaceholders.push({ latex: p1, displayMode: true });
                  return replaceBlockLatex(match, p1);
                })
                .replace(/\$([^$]+)\$/g, (match, p1) => {
                  latexPlaceholders.push({ latex: p1, displayMode: false });
                  return replaceInlineLatex(match, p1);
                })
                .replace(/(\\{1,2})begin{(\w+[*]?)}([\s\S]*?)\1end{\2}/g, (match, slashes, p1, p2) => {
                  console.log(match,"hh");
                  latexPlaceholders.push({ latex: match, displayMode: true });
                  return replaceEnvironment(match, slashes, p1, p2);
                });
            // 用showdown转换Markdown内容为HTML
            let htmlContent = converter.makeHtml(processedContent);

            // 将占位符替换回LaTeX公式并用KaTeX渲染
            latexPlaceholders.forEach((item,index) => {
              console.log("item.latex",item.latex)
                let renderedLatex;
                try {
                  if (item.displayMode) {
                        renderedLatex = Katex.renderToString(item.latex.slice(2, -2), { displayMode: true });
                    } else {
                        renderedLatex = Katex.renderToString(item.latex.slice(1, -1), { displayMode: false });
                    }
                } catch (error) {
                    renderedLatex = item.latex; // 如果解析失败，返回原始字符串
                }
                htmlContent = htmlContent.replace(`__LATEX_PLACEHOLDER_${index}__`, renderedLatex);
            });
            // 处理Markdown
            // this.renderedContent = marked(content);
            
          

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
            return htmlContent;
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
  