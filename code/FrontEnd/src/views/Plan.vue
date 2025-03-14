<!-- src/components/Plan.vue -->
<template>
    <div class="plan-container">
        <h2>旅游路线规划</h2>
        <div class="location-input">
            <input type="text"
                   placeholder="请输入目的地"
                   v-model="newLocation"
                   @keyup.enter="addLocation">
            <button @click="addLocation">添加</button>
        </div>
        <!--无序地点列表-->
        <ul class="location-list">
            <li v-for="(location, index) in locations" Key="index">
                {{location}}
                <button @click="removeLocation(index)">删除</button>
            </li>
        </ul>
        <button @click="startPlanning" :disabled="locations.length<2">开始规划</button>
        <div v-if="plannedRoute.length>0" class="planned-route">
            <h3>规划路线</h3>
            <!--有序规划路线-->
            <ol>
              <li v-for="(location,index) in plannedRoute" :key="index">{{ location }}</li>
            </ol>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default{
    name:'Plan',
    data(){
        return{
            newLocation:'',
            locations:[],
            plannedRoute:[],
        }
    },
    methods:{
        addLocation(){
          if(this.newLocation.trim()){
            this.locations.push(this.newLocation.trim());
            this.newLocation='';
          }
        },
        removeLocation(){
            this.locations.splice(index,1);
        },
        async startPlanning(){
            try{
              const response = await axios.post('http://localhost:3000/plan',{
                locations:this.locations,
              });
              this.plannedRoute = response.data;
            }catch(error){
              console.error('Error planning route:',error);
              alert('Error planning route. Please try again.');
            }
        },
    },
}
</script>

<style scoped>
.plan-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.location-input {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.location-input input {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.location-input button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.location-input button:hover {
  background-color: #0056b3;
}

.location-list {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

.location-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.location-list li button {
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  padding: 5px 10px;
}

.location-list li button:hover {
  background-color: #c82333;
}

button {
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #218838;
}

.planned-route {
  margin-top: 20px;
}

.planned-route h3 {
  margin-bottom: 10px;
}

.planned-route ol {
  padding-left: 20px;
}
</style>