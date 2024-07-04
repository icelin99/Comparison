<template>
<div style="width: 100%;">
    <div v-if="isShow" class="ct-container">
        <div>Category<MultiSelect :options="categories" v-model="selectedCategory"  optionValue="id" optionLabel="name" filter showClear @change="onCategoryChange(index)" :style="{ minWidth: '150px' }" /></div>
        <div>Tag <MultiSelect :options="tags" v-model="selectedTag"  optionValue="id" optionLabel="name" filter showClear @change="onTagChange(index)" :style="{ minWidth: '150px' }"  />
        </div>
        <div>Score <Dropdown :options="filterScores" v-model="selectedCompareScore" optionValue="value" optionLabel="label"  filter showClear  :style="{ minWidth: '150px' }" @change="onFilterScore"  />
        </div>
        <div class="select-btn-container">
            <Button  icon="pi pi-times" class="p-button-clear custom-clear-button" @click="clearData" />
            <Button icon="pi pi-search" class="p-button-query custom-query-button" @click="queryData" />
        </div>
        <div>
            <Button class="custom-mode-button" @click="changeMode">{{ isEditMode ? '切换为预览模式' : '切换为打分模式' }}</Button>
        </div>
    </div>
    <div v-if="isShow" style="display: flex; flex-direction: row; width: 100%; max-height: calc(100% - 90px); overflow: auto; position:fixed; top: 95px; bottom:65px; overflow-x:hidden;">
        <div :style="{width: '40%', height: '100%'}">
            <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'; align-items: center;">
                <div class="image-container" @dblclick="openModal('image', img_path)">
                    <img :src="img_path" alt="Can't find image">
                  </div>
                  <div v-if="isModalOpen" class="modal" @click="closeModal">
                    <span class="close"  @click="closeModal" >&times;</span>
                    <div class="modal-content" @click.stop>
                        <template v-if="modalType === 'image'">
                          <img :src="modalContent" alt="Image preview" class="img-preview"
                          @wheel="zoomImage" 
                          @mousedown="startDragging"
                          @mouseleave="stopDragging"
                            :style="imageStyle">
                        </template>
                        <template v-else>
                          <div>{{ modalContent }}</div>
                        </template>
                      </div>
                  </div>

                <div class="text-container"><div class="text-text">Category</div>
                    <div class="tag-container">
                        <div v-for="(item, index) in category" :key="index" class="tag-list">
                            <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                        </div>
                    </div>
                </div>
                <div class="text-container"><div class="text-text">Tag</div>
                    <div class="tag-container">
                        <div v-for="(item, index) in tag" :key="index" class="tag-list">
                            <Tag severity="success" :style="{backgroundColor:colorScale(item),color:'#696969'}"> {{ item }}</Tag>
                        </div>
                    </div>
                </div>
                <div class="text-container"><div class="text-text">图片地址</div><div class="image-path" @dblclick="openModal('text', pageInfo.image_path)" >{{pageInfo.image_path}}</div></div>
                <div class="text-container"><div class="text-text">问题</div><div class="text-border" @dblclick="openModal('text', pageInfo.question)"> {{pageInfo.question}}</div></div>
                <div class="text-container"><div class="text-text">参考答案</div>
                <div v-if="!isAnswerEdit" class="text-border" @dblclick="openModal('text', ref_answer)"> {{ref_answer}}</div>
                <button v-if="!isAnswerEdit && isEditMode" class="ref_answer_span" @click="handleAnswer">✏️</button>
                <InputText v-if="isAnswerEdit" class="text-border edit" v-model="editedAnswer" />
                <button v-if="isAnswerEdit && isEditMode" class="ref_answer_span" @click="handleAnswer">✔️</button>
                </div>
            </div>
        </div>
        <div :style="{width: '60%', height: '100%','max-width': '60%', 'overflow-x':'hidden'}">
            <div style="display: flex; flex-direction: row; width: '100%'; height: '100%'">
                <DataTable :value="pageInfo.modelList" stripedRows tableStyle="min-width: 50rem; overflow: scroll; white-space: normal; word-wrap: break-word; " >
                    <Column header="序号" field="index"></Column> 
                    <Column field="model_name" header="Model" style="max-width: 12rem; word-wrap: break-word;"></Column>
                    <Column field="answer" header="Answer" >
                        <template #body="{ data }">
                            <div v-html="renderMarkdown(data.answer)"></div>
                        </template>
                    </Column>
                    <Column  header="Score" >
                        <template #body="slotProps">
                            <!-- <Rating v-model="slotProps.data.standardScore" :stars="ratingStandard-1" @update:modelValue="value => onRatingChange(value,slotProps.index)">
                                <template #cancelicon>
                                    <img src="/assets/cancel.png" width="24" height="24"/>
                                </template>
                                <template #onicon>
                                    <img src="/assets/smiley.png" width="24" height="24" />
                                </template>
                                <template #officon>
                                    <img src="/assets/pensive.png" width="24" height="24" />
                                </template>
                            </Rating> -->
                            <div class="rating">
                                <template v-if="ratingStandard <= 5">
                                    <span v-for="i in ratingStandard" :key="i" @click="isEditMode ? onRatingChange(i, slotProps.index) : null"
                                          :class="{ active: slotProps.data.score !== null && slotProps.data.score !== undefined && i == reverseScaleScore(slotProps.data.score) }">
                                      {{ scaleScore(i) }}
                                    </span>
                                  </template>
                                  <template v-else>
                                    <div  class="rating-line">
                                        <div v-for="(line, index) in splitRatingStandard" :key="index">
                                            <span v-for="i in line" :key="i" @click="isEditMode ? onRatingChange(i, slotProps.index) : null"
                                                  :class="{ active: slotProps.data.score !== null && slotProps.data.score !== undefined && i == reverseScaleScore(slotProps.data.score) }">
                                              {{ scaleScore(i) }}
                                            </span>
                                          </div>
                                    </div>
                                  </template>
                            </div>
                        </template>
                    </Column>
                    <Column v-if="pageInfo.modelList.some(item => item.reason)" field="reason" header="Reason" ></Column>
                </DataTable>
               
            </div>
        </div>
    </div>
    <div v-if="isShow&&!isModalOpen" class="page-change" style="display: flex; flex-direction: column; width: '100%';">
        
        <div style="display: flex; flex-direction: row; width: '100%'; height: 30px; line-height: 25px; justify-content: center;align-items: center;">
            <Button label="" icon="pi pi-angle-left" iconPos="right" :style="{backgroundColor: leftHover?'rgba(176,196,222,0.5)': 'lightsteelblue',borderColor: 'aliceblue',marginRight:'15px'}"   @click="prevPage" @mouseover="leftHover = true" @mouseleave="leftHover = false" />
            Page {{ currentPage }} of {{ pageCount }}
            <Button label=""  icon="pi pi-angle-right"  :style="{backgroundColor: rightHover? 'rgba(100,149,237,0.5)':'cornflowerblue',borderColor: 'aliceblue'}"   @click="nextPage" @mouseover="rightHover = true" @mouseleave="rightHover = false" />
            <p> 跳转 </p>
            <InputNumber v-model="jumpPage" inputId="minmax-buttons" mode="decimal" :min="1" :max="pageCount" @keyup.enter="jump" autofocus />
                <Button style="margin-left: 10px; background-color: cornflowerblue;" v-if="isEditMode && !saveAllClick && currentPage == pageCount" label="Save All"     @click="saveAllPage" />
                <Button style="margin-left: 10px; background-color: cornflowerblue;" v-if="isEditMode && saveAllClick && currentPage == pageCount" label="All saved ✔️" disabled="true" />
         
        </div>
        
    </div>
    <Toast ref="toast" />
</div>
</template>

<script>
import * as d3 from 'd3'
import {mapGetters, mapMutations} from "vuex"
import Button from 'primevue/button'
import InputNumber from 'primevue/inputnumber'
import Tag from 'primevue/tag'
import Rating from 'primevue/rating'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import api from '@/utils/api'
import MarkdownIt from 'markdown-it'
import markdownItTable from 'markdown-it-multimd-table';
import markdownItContainer from 'markdown-it-container';
import katex from 'katex';
import MultiSelect from 'primevue/multiselect'
import Dropdown from 'primevue/dropdown'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Toast from 'primevue/toast'
// import markdownItKatex from 'markdown-it-katex'
import 'katex/dist/katex.min.css';
// import { renderMarkdown } from '../utils/markdownCompile.js';
import CodeBlockRenderer from './CodeBlockRenderer.vue'
import hljs from 'highlight.js';
import 'highlight.js/styles/default.css';
import { marked } from 'marked';
import showdown from 'showdown';
import showdownKatex from 'showdown-katex';


export default {
    name: 'App',
    components: {
        Button,
        InputNumber,
        Tag,
        Rating,
        DataTable,
        Column,
        MultiSelect,
        Dropdown,
        Dialog,
        InputText,
        Toast,
        CodeBlockRenderer
    },
    computed: {
        ...mapGetters(["selectSubmitted","currentData", "pageCount", "currentPage","ratingStandard", "pageInfo", "categoryList", "tagList","dataInfoList"]),
        splitRatingStandard() {
            // Split the array into two halves
            const rating = Array.from({ length: this.ratingStandard }, (_, index) => index + 1);
            
            const midpoint = Math.ceil(this.ratingStandard / 2);
            console.log("splitratingstandard",rating,rating.slice(0, midpoint),rating.slice(midpoint))
            return [
                rating.slice(0, midpoint),
                rating.slice(midpoint)
            ];
        },
    },
    mounted() {
        this.$store.dispatch('updateIsLoading', false); // 挂载完成，隐藏loading
        window.addEventListener("keydown",this.handleKeydown);
        this.getCategoryList();
        this.getTagList();
    },
    beforeDestroy() {
        window.removeEventListener("keydown",this.handleKeydown);
    },
    watch: {
        selectSubmitted(newVal) {
            this.selectedCategory = null;
            this.selectedTag = null;
            this.selectedCompareScore = null;
            this.getCategoryList();
            this.getTagList();
            console.log("submittted and show!");
            if(newVal == true) {
                this.isShow = true;
                const selectModels = JSON.parse(localStorage.getItem("modelIDs"));
                console.log("select models",selectModels);
                if(selectModels.length == 2) {
                    if(this.ratingStandard == 3) {
                        this.filterScores = [{ label: '0', value: 0 }, { label: '1', value: 0 },{ label: '模型1分数更高', value: -1 }, { label: '模型2分数更高', value: -2 }];
                    } else if(this.ratingStandard == 5) {
                        this.filterScores = [{ label: '0', value: 0 }, { label: '4', value: 4 },{ label: '模型1分数更高', value: -1 }, { label: '模型2分数更高', value: -2 }];
                    } else if(this.ratingStandard == 10) {
                        this.filterScores = [{ label: '0', value: 0 }, { label: '9', value: 9 },{ label: '模型1分数更高', value: -1 }, { label: '模型2分数更高', value: -2 }];
                    }
                } else {
                    if(this.ratingStandard == 3) {
                        this.filterScores = [{ label: '0', value: 0 }, { label: '1', value: 0 }];
                    } else if(this.ratingStandard == 5) {
                        this.filterScores = [{ label: '0', value: 0 }, { label: '4', value: 4 }];
                    } else if(this.ratingStandard == 10) {
                        this.filterScores = [{ label: '0', value: 0 }, { label: '9', value: 9 }];
                    }
                }
                console.log("filter score",this.filterScores)
            } else {
                this.isShow = false;
            }
        },
        pageInfo(newVal) {
            console.log("pageInfo", newVal);
        
            this.img_path = newVal.image_code;
            this.tag = newVal.tags;
            this.category = newVal.categories;
            // this.modelList = {};
            // if(newVal && newVal.modelList && newVal.modelList.length){
            //     const _newVal = JSON.parse(JSON.stringify(newVal))
            //     console.log(_newVal.modelList[0] === newVal.modelList[0])
            //     this.localModelList = _newVal.modelList;
            // }
            this.data_info_id = newVal.data_info_id;
            this.ref_answer = newVal.ref_answer;

        },
        currentPage(newVal) {
            console.log("current page",newVal)
        },
        categoryList(newVal) {
            this.selectedCategory = null;
            console.log("getting new category list", newVal);
            this.categories = newVal;
            console.log(this.categories)
        },
        tagList(newVal) {
            this.selectedTag = null;
            console.log("getting new tag list", newVal);
            this.tags = newVal;
        },
        pageCount(newVal) {
            console.log("new page count",newVal)
        },
        ratingStandard(newVal) {
            if(newVal == 3) {
                this.filterScores = [0,1];
            } else if(newVal == 5) {
                this.filterScores = [0,4];
            } else if(newVal == 10) {
                this.filterScores = [0,9];
            }
            console.log("filter score",this.filterScores)
        }
    },
    created() {
        this.markdownItInstance = new MarkdownIt({
            html: true, // 允许 HTML 标签
            breaks: true, // 将 \n 转换为 <br>
            linkify: true, // 自动将 URL 转为链接
        })
        .use(markdownItTable)
        .use(markdownItContainer)
        // .use(markdownItKatex, {
        //     inlineRenderer: (fragment, options, displayMode) => {
        //     console.log(fragment,options,displayMode)
        //     return Katex.renderToString(fragment, options.displayMode)
        //     }
        // });
    },
    data() {
        return {
            isShow: false,
            data: null,
            // modelList: [],
            scoreList: [0,0.5,1],
            selectedScore: null,
            imagePath: "/assets/scenery.jpeg",
            question: "How is the view in this picture?",
            tag: null,
            // ["好", "图片", "经典", "景点", "任务", "人物", "场景", "风景", "美食", "娱乐", "智能"],
            category: null,
            jumpPage: null,
            leftHover: false,
            rightHover: false,
            colorScale: d3.scaleOrdinal(d3.schemePastel1),
            saveOneClick: false,
            saveAllClick: false,
            img_path: "",
            data_info_id: null,
            scrollInterval: null,
            markdownItInstance: null,
            isModalOpen: false,
            modalType: 'text', // 'text' or 'image'
            modalContent: '', // Content to display in modal
            selectedCategory: null,
            selectedTag: null,
            categories: [],
            tags: [],
            zoomLevel: 1,
            isDragging: false,
            startX: 0,
            startY: 0,
            translateX: 0,
            translateY: 0,
            imageStyle: {
                transform: 'scale(1)  translate(0px, 0px)',
                cursor: 'grab'
            },
            pageEdit: [],
            editedAnswer: "",
            isAnswerEdit: false,
            ref_answer: "",
            isEditMode: false,
            filterScores: [],
            selectedCompareScore: null,
            data_info_list: []
        }
    },
    methods: {
        ...mapMutations(['nextItem','prevItem','setPage']),
        startScroll(event) {
            console.log("event",event.target);
            event.target.classList.add('scrollable');
        },
        stopScroll(event) {
            console.log("event",event.target);
            event.target.classList.remove('scrollable');
            // clearInterval(this.scrollInterval); // 停止滚动
        },
        startDrag(event) {
            this.isDragging = true;
            this.startX = event.pageX - event.target.offsetLeft;
            this.scrollLeft = event.target.scrollLeft;
            event.target.style.cursor = 'grabbing'; // 改变鼠标指针为抓取状态
        },
        stopDrag(event) {
            this.isDragging = false;
            event.target.style.cursor = 'grab'; // 恢复鼠标指针为抓手状态
        },
        drag(event) {
            if (!this.isDragging) return;
            event.preventDefault();
            const x = event.pageX - event.target.offsetLeft;
            const walk = x - this.startX; // 计算鼠标移动距离
            event.target.scrollLeft = this.scrollLeft - walk; // 滚动内容
        },
        openModal(type, content) {
            this.modalType = type;
            this.modalContent = content;
            this.isModalOpen = true;
            this.zoomLevel = 1;
            this.translateX = 0;
            this.translateY = 0;
            this.updateImageStyle();
        },
        closeModal() {
        this.isModalOpen = false;
        },
        // renderMarkdown(content) {
        //     // console.log(content)
        //     if(content == null){
        //         return null;
        //     }
        //     // 去掉字符串中的\n
        //     const sanitizedInput = content.replace(/\\n/g, '\n').replace(/^```markdown/, '').replace(/```$/, '').replace(/```/g, '\\`\\`\\`');
        //     console.log("处理后的代码",sanitizedInput)
        //     return this.markdownItInstance.render(sanitizedInput);
        // },
        renderMarkdown(content) {
            if(content == null) {
                return ""
            }
            // 处理代码块
            content = content.replace(/```([\s\S]*?)\n([\s\S]*?)```/g, function(match, lang, code) {
                console.log("Matched language:", lang, code);
                if (lang.trim() === 'latex' || lang.trim() === 'asciimath') {
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
                        return katex.renderToString(`\\begin{${p1}}${p2}\\end{${p1}}`, { displayMode: true });
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
                        renderedLatex = katex.renderToString(item.latex.slice(2, -2), { displayMode: true });
                    } else {
                        renderedLatex = katex.renderToString(item.latex.slice(1, -1), { displayMode: false });
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
        handleKeydown(event) {
            if (event.key === "ArrowLeft") {
                this.prevPage();
            } else if(event.key == "ArrowRight") {
                this.nextPage();
            }
        },
        async nextPage() {
            // 获取下一页数据
            const page = this.currentPage + 1;
            this.saveAndGet(page);
        },
        async prevPage() {
            // 获取上一页数据
            const page = this.currentPage - 1;
            this.saveAndGet(page);
        },
        async jump() {
            console.log("jump page",this.jumpPage);
            this.saveAndGet(this.jumpPage,true);
        },
        scaleScore(standardScore) {
            let scale = null;
            console.log("sclae score",this.ratingStandard)
            if(this.ratingStandard == 3) {
                scale = d3.scaleOrdinal().domain([1,2,3]).range([0,0.5,1])
            } else if(this.ratingStandard == 5) {
                scale = d3.scaleOrdinal().domain([1,2,3,4,5]).range([0,1,2,3,4])
            } else {
                // 10
                scale = d3.scaleOrdinal().domain([1,2,3,4,5,6,7,8,9,10]).range([0,1,2,3,4,5,6,7,8,9])
            }
            return scale(standardScore);
        },
        reverseScaleScore(score) {
            let scale = null;
            if(this.ratingStandard == 3) {
                scale = d3.scaleOrdinal().domain([0,0.5,1]).range([1,2,3])
            } else if(this.ratingStandard == 5) {
                scale = d3.scaleOrdinal().domain([0,1,2,3,4]).range([1,2,3,4,5])
            } else {
                scale = scale = d3.scaleOrdinal().domain([0,1,2,3,4,5,6,7,8,9]).range([1,2,3,4,5,6,7,8,9,10])
            }
            return scale(score);
        },
        onRatingChange(score, index) {
            console.log('model list index, score', index, score)

            const save_score = this.scaleScore(score)
            this.pageInfo.modelList[index].score = save_score;
            // 记录修改的索引
            if (!this.pageEdit.includes(index)) {
                this.pageEdit.push(index);
            }
           
        },
        saveOnePage() {
            this.saveOneClick = true;
            //  save to databse
        },
        saveAllPage() {
            this.saveAllClick = true;
            // save all to database
        },
        async saveAndGet(nextPage,isJump=false) {
            const model_l = this.pageInfo.modelList;
            if(this.isEditMode && this.pageEdit && this.pageEdit.length && this.pageEdit.length > 0) {
                // 保存本页数据
                const modelList = this.pageEdit.map(index => ({
                    "modelID": model_l[index].model_id,
                    "score": model_l[index].score,
                    "standard": parseInt(localStorage.getItem("standard"),10)
                }))
                console.log("修改了的model list",modelList)
                try {
                    const res = await api.saveById(this.currentPage,this.data_info_id, modelList);
                    console.log("save",res.data.message);
                }
                catch (error) {
                    console.error('Error save this page:', nextPage, error)
                }
            }
            if(nextPage >= 1 && nextPage <= this.pageCount) {
                this.$store.dispatch("updateCurrentPage", nextPage);
                this.$store.dispatch("updateIsLoading", true);
                try {
                    const data_info_list = JSON.parse(localStorage.getItem("data_info_list"));
                    const info_id = data_info_list[nextPage-1];
                    console.log("get data by datainfo id",data_info_list,info_id);
                    const response = await api.getPageById(info_id,JSON.parse(localStorage.getItem("modelIDs")),parseFloat(this.selectedCompareScore));
                    console.log(" page info",response.data);
                    this.$store.dispatch("updateIsLoading", false);
                    this.$store.dispatch("updatePageInfo", response.data["page_info"]);
                    if(isJump) {
                        this.jumpPage = null;
                    }
                    this.pageEdit = [];
                }
                catch (error) {
                    console.error('Error getting page:', error)
                }
            }
            
        },
        async getTagList(catregoryIds=[]) {
            try {
                const response = await api.getTagList(parseInt(localStorage.getItem("datasetID"),10), JSON.parse(localStorage.getItem("modelIDs")),catregoryIds);
                console.log("response",response.data);
                this.tags = response.data;
            }
            catch (error) {
                console.error('Error getting tag list:', error)
            }
        },
        async getCategoryList(tagIds = []) {
            try {
                const response = await api.getCategoryList(parseInt(localStorage.getItem("datasetID"),10), JSON.parse(localStorage.getItem("modelIDs")),tagIds);
                console.log("response",response.data);
                this.categories = response.data;
            }
            catch (error) {
                console.error('Error getting category list:', error)
            }
        },
        onTagChange() {
            console.log("select tag:",this.changeObject2List(this.selectedTag));
            if(this.selectedTag) {
                
                const tag_list = this.changeObject2List(this.selectedTag);
                console.log("!!!!!!!!!!!!!!!! xuan ze le", tag_list)
                this.getCategoryList(tag_list);
            } else {
                this.getCategoryList()
            }
        },
        onCategoryChange() {
            console.log("select:",this.changeObject2List(this.selectedCategory));
            if(this.selectedCategory) {
                const category_list = this.changeObject2List(this.selectedCategory);
                this.getTagList( category_list);
            } else {
                this.getTagList();
            }
        },
        changeObject2List(object) {
            console.log(object, Object.values(object))
            return Object.values(object);
        },
        zoomImage(event) {
            const scaleAmount = 0.1;
            if (event.deltaY < 0) {
                this.zoomLevel += scaleAmount;
            } else {
                this.zoomLevel -= scaleAmount;
                if (this.zoomLevel < 1) {
                    this.zoomLevel = 1;
                }
            }
            this.updateImageStyle();
        },
        startDragging(event) {
            console.log("start dragging",this.zoomLevel)
            event.preventDefault();
            if (this.zoomLevel > 1) {
                this.isDragging = true;
                this.startX = event.clientX - this.translateX;
                this.startY = event.clientY - this.translateY;
                this.imageStyle.cursor = 'grabbing';
                window.addEventListener('mousemove', this.dragImage);
                window.addEventListener('mouseup', this.stopDragging);
            }
        },
        dragImage(event) {
            
            if (this.isDragging) {
                console.log("dragImage",event)
                this.translateX = event.clientX - this.startX;
                this.translateY = event.clientY - this.startY;
                this.updateImageStyle();
            }
        },
        stopDragging() {
            if (this.isDragging) {
                this.isDragging = false;
                this.imageStyle.cursor = 'grab';
            }
        },
        updateImageStyle() {
            this.imageStyle.transform = `scale(${this.zoomLevel}) translate(${this.translateX}px, ${this.translateY}px)`;
        },
        clearData() {
            this.selectedCategory = null;
            this.selectedTag = null;
            this.getCategoryList();
            this.getTagList();
            this.selectedCompareScore = null;
            this.queryData();
        },
        async queryData() {
            let category_list = null;
            if(this.selectedCategory && this.selectedCategory.length> 0) {
                category_list = this.changeObject2List(this.selectedCategory);
            }
            let tag_list = null;
            if(this.selectedTag && this.selectedTag.length > 0) {
                tag_list = this.changeObject2List(this.selectedTag);
            } 
            try {
                this.$store.dispatch('updateIsLoading', true);
                this.$store.dispatch("updateCurrentPage",1);
                const res = await api.getFilterList(parseInt(localStorage.getItem("datasetID"),10),JSON.parse(localStorage.getItem("modelIDs")),tag_list,category_list,parseFloat(this.selectedCompareScore));
                console.log("query data",res.data);
                this.$store.dispatch("updateDataInfoList",res.data["data_info_list"]);
                this.$store.dispatch("updatePageCount",res.data["page_count"]);
                this.$store.dispatch("updatePageInfo",res.data["page_info"]);
                this.$store.dispatch('updateIsLoading', false);
            }
            catch (error) {
                console.error('Error getting filter list and first page:', error)
            }
            
        },
        async handleAnswer() {
            console.log("edit answer", this.isAnswerEdit, this.ref_answer,this.editedAnswer);
            if(this.isAnswerEdit) {
                if(this.isEditMode) {
                    // 如果没做修改，不上传
                    if(this.editedAnswer !== this.ref_answer) {
                        // 保存并上传
                        this.ref_answer = this.editedAnswer;
                        this.$store.dispatch("updateIsLoading", true);
                        try {
                            const res = await api.editAnswer(this.data_info_id, this.editedAnswer);
                            console.log(res);
                            if(res.data["error"]) {
                                this.showToast('error','Error', res.data["error"])
                            }
                            this.$store.dispatch("updateIsLoading",false);
                        }
                        catch(err) {
                            console.log("修改ref answer",err);
                        }
                    }
                    
                }
                
            } else {
                this.editedAnswer = this.ref_answer
            }
            this.isAnswerEdit = !this.isAnswerEdit;
            
        },
        showToast(severity,summary,detail){
            this.$refs.toast.add({ severity: severity, summary: summary, detail: detail, life: 2000 })
        },
        changeMode() {
            this.isEditMode = !this.isEditMode;
        },
        onFilterScore() {
            console.log(this.selectedCompareScore, this.filterScores)
        }
    }
}
</script>

<style>
.model-container {
    display: flex;
    justify-content: center;
    /* margin-bottom: 10px; */
}
.mode-name {
    width: 20%;
}
.model-answer {
    width: 60%;
}
.model-score {
    max-height: 40px;
    align-items: center;
    padding: 1px 2px 1px 2px;
    width: 20%;
}
.image-container {
    width: 450px;
    overflow: hidden;
    cursor: pointer;
}
.image-container  img {
    width: 98%;
    object-fit: contain;
    transition: transform 0.3s ease;
}
.modal {
    display: flex;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.9);
    align-items: center;
    justify-content: center;
}
.close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #fff;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
}
.modal-content {
    margin: auto;
    display: block;
    max-width: 80%;
    max-height: 80%;
}
.text-container {
    width: 98%;
    display: flex;
    flex-direction: row;
    margin-top: 10px;
    padding: 5px 0;
    overflow: hidden;
    align-items: center;
   /* position: relative; */
}
.text-border {
    border: 1px solid skyblue;
    border-radius: 5px;
    padding: 5px;
    /*margin-left: 20px; */
    background-color: rgba(135,206,250,0.6);
   /* position: absolute; */
    /* left: 75px; */
    cursor: pointer;
   
}
.edit {
    flex-grow: 1;
}
.page-change {
    bottom: 0;
    padding: 15px 0 10px 5px;
    align-items: center;
    margin: auto;
    justify-content: center;
    position: fixed;
    width: 100%;
    height: 65px;
    margin-bottom: 8px;
}
.page-change p {
    margin-left:50px;
}
.tag-container {
    display: flex;
    flex-wrap: wrap; /* 允许元素在需要时换行 */
    
  }
.tag-list {
    /* margin-left: 15px; */
    padding-left: 5px;
}
.rating-img {
    width: 24px;
    height: 24px;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
}
.rating-img img {
    width: 100%;
    height: 100%;
}
.save-button {
    padding-bottom: 30px;
    padding-right: 20px;
    padding-left: 20px;
}
.rating {
    display: inline-flex;
}

.rating-line {
    display: flex;
    justify-content: space-between;
    flex-direction: column;
}

.rating span {
    cursor: pointer;
    margin: 0 2px 0 2px;
    font-size: 20px;
    color: #9e9e9e;
    min-width: 24px;
    border: none;
    border-radius: 5px;
    background-color: rgb(255, 255, 255);
    justify-items: center;
    align-items: center;
    padding: 0 3px;
}

.rating span.active {
    color: #f44336;
    background-color: rgb(233, 243, 251);
    font-weight: bold;
    border: 1px solid #b4b4b4;
}

.image-path {
    white-space: nowrap;
    cursor: pointer;
    border: 1px solid #b9d4e6;
    background-color: rgba(135,206,250,0.6);
    border-radius: 5px;
    padding: 5px;
    /*margin-left: 20px;
    left: 70px; */
    overflow: hidden;
}
.scrollable {
    animation: scrollText 5s linear infinite; /* 设置滚动动画 */
}
.modal {
    display: flex;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(198, 198, 198, 0.9);
    align-items: center;
    justify-content: center;
}
.close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #fff;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
} 
.modal-content img {
    margin: auto;
    display: block;
    max-width: 90vw; /* 最大宽度为视口宽度的90% */
    max-height: 90vh; /* 最大高度为视口高度的90% */
    object-fit: contain; /* 保持纵横比并适应容器 */
}
.modal-content {
    margin: auto;
    display: block;
    max-width: 80%;
    max-height: 80%;
    color: white; /* 如果是文本内容，则设置文本颜色为白色 */
    background-color: rgba(255, 255, 255, 0); /* 设置背景颜色为黑色 */
    padding: 20px; /* 为文本内容添加一些内边距 */
    font-size: 3rem;
  }
@keyframes scrollText {
    0% {
        transform: translateX(100%);
    }
    100% {
        transform: translateX(-100%);
    }
}
.text-text {
    min-width: 75px;
    font-weight: bold;
    height: 20px;
    line-height: 15px;
    text-align: start;
}
.ct-container {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #ddd;
    height: 50px;
    top:45px;
    position:fixed;
    width: 100%;
    padding-left: 200px;
    padding-right: 200px;
    font-family: 'Arial', sans-serif; 
    font-weight: bold;
    padding-top:5px;
}

.select-btn-container {
    display: flex;
    gap:1rem;
    align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  padding-bottom:7px;
}
.custom-clear-button {
    background-color: #fbd6d6; 
    border-color: #e9d6d6;
    color: rgb(84, 84, 84);
}
  
.custom-clear-button:hover {
    background-color: #fff3f3; 
}
  
.custom-query-button {
    background-color: #dceeff; 
    border-color: #edf6ff;
    color: rgb(84, 84, 84);
}
  
.custom-query-button:hover {
    background-color: #f1f8ff; 
}

.custom-mode-button {
    background-color: #FFFACD;
    border-color: #fefbe0;
    margin-right: 10px;
    color: rgb(84, 84, 84);
    border-left: 20px;
}
.custom-mode-button:hover {
    background-color: #fffdeb;
}
.ref_answer_span {
    border-radius: 50%;
    border: 1.5px solid #dceeff;
    width: 28px;
    height: 28px;
}
</style>
<style scoped>

::v-deep .p-dropdown {
  height: 36px !important; /* Set your desired item height */
  align-items: center;
}
::v-deep .p-multiselect {
    height: 36px !important; /* Set your desired item height */
    align-items: center;
  }
::v-deep .p-button {
    transition: background-color 0.3s !important; 

}
::v-deeep .p-button:hover {
    background-color: #f1f5f9 !important;
}
::v-deep .p-inputtext {
    margin-left:10px;
    width: 50px;
}
::v-deep .p-rating {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
::v-deep .p-rating-item{
    margin-right: 2px;
    padding: 0;
    width: 24px;
    height: 24px;
    box-sizing: border-box;
    flex-basis: 24px;
}
::v-deep .p-datatable {
    width: 100%;
}

::v-deep .p-tag {
    font-size: 0.9rem;
}

</style>
    