<!-- src/components/Swiper.vue -->
<template>
  <div class="swiper">
    <div class="swiper-content" ref="swiperContent">
      <div class="swiper-item" v-for="(item, index) in imageurl" :key="index">
        <img :src="item" alt="" />
      </div>
    </div>
    <div class="page" ref="pageContainer">
      <span 
        v-for="(item, index) in imageurl" 
        :key="index" 
        @click="handlePageClick(index)"
        :class="{ active: currentIndex === index }"
      ></span>
    </div>
  </div>
</template>
  
<script>
import testImage1 from '../assets/bupt.jpg';
import testImage2 from '../assets/bupt2.jpg';
import testImage3 from '../assets/bnuz.jpg';

export default {
  name: 'swiper',
  data() {
    return {
      imageurl: [
        testImage1,
        testImage2,
        testImage3
      ],
      currentIndex: 0,
      timer: null,
      slideWidth: 800,
      autoPlayInterval: 3000,
      restartTimer: null
    }
  },
  mounted() {
    this.startAutoPlay();
  },
  beforeUnmount() {
    this.stopAutoPlay();
    if(this.restartTimer){
      clearTimeout(this.restartTimer);
    }
  },
  methods: {
    handlePageClick(index) {
      this.stopAutoPlay();
      this.currentIndex = index;
      this.updateSlidePosition();

      // Clear timer
      if(this.restartTimer) {
        clearTimeout(this.restartTimer);
        this.restartTimer = null;
      }
      
      // Resume auto play after delay
      setTimeout(() => {
        this.startAutoPlay();
      }, 2000);
    },
    
    updateSlidePosition() {
      if (this.$refs.swiperContent) {
        this.$refs.swiperContent.style.left = -this.slideWidth * this.currentIndex + 'px';
      }
    },
    
    updatePageIndicator() {
      if (this.$refs.pageContainer && this.$refs.pageContainer.children) {
        Array.from(this.$refs.pageContainer.children).forEach((item, index) => {
          item.style.backgroundColor = index === this.currentIndex ? 'red' : 'white';
        });
      }
    },
    
    startAutoPlay() {
      this.stopAutoPlay();

      this.timer = setInterval(() => {
        this.currentIndex++;
        if (this.currentIndex > this.imageurl.length - 1) {
          this.currentIndex = 0;
        }
        this.updateSlidePosition();
        this.updatePageIndicator();
      }, this.autoPlayInterval);
    },
    
    stopAutoPlay() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    }
  },
  watch: {
    currentIndex() {
      this.updatePageIndicator();
    }
  }
}
</script>

<style scoped>
.swiper {
  height: 400px;
  width: 800px;
  position: relative;
  overflow: hidden;
  margin: 50px auto;
  border: 10px solid blue;
  border-radius: 10px;
}

.swiper-content {
  position: absolute;
  left: 0;
  display: flex;
  transition: all 0.7s;
}

.swiper-item {
  width: 800px;
  height: 400px;
}

img {
  width: 100%;
  height: 100%;
}

.page {
  position: absolute;
  left: 50%;
  transform: translate(-50%, 50%);
  bottom: 15px;
}

span {
  display: inline-block;
  height: 15px;
  width: 15px;
  background-color: white;
  margin-left: 20px;
  border-radius: 200px;
  cursor: pointer;
}

span.active {
  background-color: red;
}
</style>

