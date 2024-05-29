<template>
    <div class="markdown-editor">
      <textarea v-model="input" placeholder="Enter Markdown text here..."></textarea>
      <div v-html="compiledMarkdown" class="preview"></div>
    </div>
</template>
  
<script>
import MarkdownIt from 'markdown-it';
import markdownItTable from 'markdown-it-multimd-table';
import markdownItContainer from 'markdown-it-container';

  
export default {
    data() {
      return {
        input: '',
      };
    },
    computed: {
      compiledMarkdown() {
            // 保存代码块并处理其他内容
        // let content = this.input;
        // const codeBlocks = [];
        // content = content.replace(/```(.*?)```/gs, (match, p1) => {
        //   codeBlocks.push(match);
        //   return `CODE_BLOCK_${codeBlocks.length - 1}`;
        // });

        // // 处理表格和其他内容
        // const sanitizedInput = content.replace(/```markdown/g, '').replace(/```/g, '');
        // const markdown = new MarkdownIt({ breaks: true }).use(markdownItTable);
        // let renderedContent = markdown.render(sanitizedInput.trim());

        // // 恢复代码块
        // renderedContent = renderedContent.replace(/CODE_BLOCK_(\d+)/g, (match, p1) => {
        //   return codeBlocks[p1];
        // });

        // return renderedContent;
        // 初始化 markdown-it 并使用 markdown-it-container 插件
        const sanitizedInput = this.input.replace(/\\n/g, '\n').trim();
        const markdown = new MarkdownIt({ breaks: true })
          .use(markdownItTable)
          .use(markdownItContainer, 'markdown', {
            validate: params => params.trim() === 'markdown',
            render: (tokens, idx) => {
              const token = tokens[idx];
              if (token.nesting === 1) {
                // Opening tag
                return '<div class="markdown-it-container">\n';
              } else {
                // Closing tag
                return '</div>\n';
              }
            }
          });

        return markdown.render(sanitizedInput);
      }
    }
};
</script>
  
<style scoped>
.markdown-editor {
    display: flex;
    gap: 20px;
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
  