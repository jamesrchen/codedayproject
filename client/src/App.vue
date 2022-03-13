<template>
  <InputText style="width:70vw" v-on:keyup.enter="getReviews" v-model="name" />
  <Panel id="review" v-for="review in reviews" :key="review.summary" :header="'Sentiment: '+review.sentiment">
      <div style="display: flex;">
        <p style="text-align:left">{{review.summary}}</p>
        <img style="height:400px;width:400px;margin-left:50px" :src="'http://localhost/wordclouds/'+review.wordcloud" />
      </div>
  </Panel>
  <div/>
</template>

<script>
import axios from 'axios';

let API = axios.create({
  baseURL: 'http://localhost:80',
})

export default {
  name: 'App',
  components: {
  },
  data() {
    return {
      name: '',
      reviews: []
    }
  },
  methods: {
    getReviews() {
      console.log(this.name)
      API.get(`/data/${this.name}`)
        .then(response => {
          this.reviews = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
}
</script>

<style>
#app {
  padding-left: 10vw;
  padding-right: 10vw;
  text-align: center
}

#review {
  margin: 5vh
}
</style>
