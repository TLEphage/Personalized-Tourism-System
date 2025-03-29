<!-- views/Recommend.vue -->
<template>
    <div class="Recommend">
        <h2>精彩纷呈</h2>
        <swiper/>
        <div class="ranking">
            <h2>热门景点</h2>
            <ul>
                <li v-for="(spot,index) in rankingList" :key="index" @click="gotoDetailPage(spot.id)">
                    <img  alt="spot.name">
                    <p>{{ spot.name }}</p>
                </li>
            </ul>
        </div>
    </div>

</template>

<script>
import swiper from '../components/swiper.vue';
export default{
    name:'Recommend',
    data(){
        return{
            rankingList:[],
        }
    },
    components:{
        swiper,
    },
    mounted(){
        this.fetchRankingList();
    },
    methods:{
        fetchRankingList(){
            this.rankingList=[
                {id:1,name:'spot1',image:"../assets/bupt.jpg"},
            ]
        },
        gotoDetailPage(spotId){
            //this.$router.push({name:'Detail',params:{spotId}});
            console.log(`Go to detail page with spotId: ${spotId}`);
        }
    }
}
</script>

<style>
.Recommend{
    width: 100%;
    height: 100%;
}
.ranking {
  margin-top: 20px;
  padding: 10px;
}

.ranking h2 {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
}

.ranking ul {
  list-style-type: none;
  padding: 0;
}

.ranking li {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  cursor: pointer;
}

.ranking .spot {
  display: flex;
  align-items: center;
}

.ranking .spot img {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.ranking .spot p {
  font-size: 18px;
}
</style>