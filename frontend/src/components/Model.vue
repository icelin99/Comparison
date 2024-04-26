<template>
    <div>
        <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'">
            <div class="model-container" v-for="(item, index) in modelList" :key="index" >
                <div class="model-name">{{ item.model }}</div>
                <div class="model-answer">{{ item.answer }}</div>
                <div class="model-score">
                    <Dropdown style=" width: 150px; line-height: 30px;"  placeholder="scoring for this model performance" v-model="selectedScore" :options="scoreList" />
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import Dropdown from 'primevue/dropdown'

export default {
    name: 'App',
    components: {
        Dropdown
    },
    data() {
        return {
            modelList: [{
                "model": "model 1",
                "answer": "The view in this picture is serene, with the calm, clear waters reflecting the tranquility of nature. The boat glides gently, offering a peaceful respite from the hustle of daily life.",
                "score": 0
            }, {
                "model": "model 2",
                "answer": "This image captures the stunning clarity of the water, a testament to the pristine environment. The vivid greenery and the cascading waterfall in the background create a picturesque scene of natural beauty.",
                "score": 0.5
            }, {
                "model": "model 3",
                "answer": "It's a breathtaking view that showcases the harmony between humans and nature. The traditional boat and the person's attire suggest a cultural depth, adding a layer of richness to the already visually captivating landscape.",
                "score": 0
            }, {
                "model": "model 4",
                "answer": "The photograph offers a glimpse into a world that appears untouched by time, where the purity of the water and the lushness of the surrounding foliage speak of a hidden paradise.",
                "score": 1
            }, {
                "model": "model 5",
                "answer": "This view is like a painting come to life, where every element conspires to evoke a sense of wonder. The waterfall adds a sense of grandeur to the scene, making it not just a picture, but an experience for the viewer.",
                "score": 0.5
            }],
            scoreList: [0,0.5,1],
            selectedScore: 0,
        }
    }
}
</script>

<style>
.model-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}
.model-container div {
    flex: 1;
    text-align: center;
    padding: 10px;
}
.model-score {
    max-height: 40px;
    align-items: center;
}
</style>
<style scoped>

::v-deep .p-dropdown {
  height: 50px !important; /* Set your desired item height */
  align-items: center;
}
</style>