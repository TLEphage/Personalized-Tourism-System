<!-- views/Recommend.vue -->
<template>
    <div class="Recommend">
        <h2>精彩纷呈</h2>
        <swiper/>
        <div class="ranking">
            <h2>热门景点</h2>
            <ul>
                <li v-for="(spot,index) in rankingList" :key="index" @click="gotoDetailPage(spot.id)" class="spot">
                    <img  alt="景点照片" :src="spot.image">
                    <p>{{ spot.name }}</p>
                </li>
            </ul>
        </div>
    </div>

</template>

<script>
// 景点数据结构
// name:String
// id:Int16Array,
// image:jpg/png/...,可以是数组
// rating:float,
// lng,lat:float,经纬度
// type:String,如山水，公园，古迹等
// content:stirng,具体的景点描述
// link: 整型数组，展示景点相关的日记


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
                {id:1,name:'北京邮电大学',image:"https://inews.gtimg.com/om_bt/O9MxUvbYy398K4oy9xqTlJofhwUlrVZU-FNauSwRNEss8AA/641"},
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
  width: 400px;
  height: 200px;
  margin-right: 10px;
}

.ranking .spot p {
  font-size: 18px;
}
</style>