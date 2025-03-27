<!-- src/components/GitHubLink.vue -->
 <template>
    <a 
        href="https://github.com/TLEphage/Beijing-Navigation-System"
        target="_blank"
        class="github-link">
        <img src="../assets/github.png" 
            alt="GitHub Logo" class="github-icon" @error="handleImageError">
        <span v-if="imageError">GitHub Logo</span>
    </a>
 </template>

<script>
export default{
    name:'GitHubLink',
    data(){
        return {
            imageError:false,
        }
    },
    methods:{
        handleImageError(){
            this.imageError=true;
        }
    },
}
</script>

<style scoped> 
.github-link{
    position:fixed;
    top:10px;
    left:10px;
    z-index:1000;
}
.github-icon{
    width:32px;
    height:32px;
}
</style>