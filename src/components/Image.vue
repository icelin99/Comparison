<template>
    <div>
        <div style="display: flex; flex-direction: column; width: '100%'; height: '100%'; align-items: center;">
            <div class="image-container"><img :src="imagePath" alt="Can't find image"></div>
            <div class="text-container"><div>Question: </div><div class="text-border"> {{question}}</div></div>
            <div class="text-container"><div>Tag: </div><div class="text-border"> {{ tag }}</div></div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'App',
    components: {
    },
    data() {
        return {
            imagePath: "/assets/scenery.jpeg",
            question: "How is the view in this picture?",
            tag: "tag of the dataset"
        }
    }
}
</script>

<style>
.image-container {
    width: 400px;
    height: 400px;
    overflow: hidden;
}
.image-container  img {
    width: 98%;
    height: 98%;
    object-fit: cover;
}
.text-container {
    width: 98%;
    display: flex;
    flex-direction: row;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 5px;
    padding-bottom: 5px;
    align-items: center;
}
.text-border {
    border: 1px solid skyblue;
    border-radius: 5px;
    padding: 5px;
    margin-left: 20px;
}
</style>
    