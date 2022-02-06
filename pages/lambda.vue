<template>
  <div>
    <h1>Images</h1>
    <!-- <p>{{ message }}</p> -->
    <v-list>
      <v-list-item v-for="url in urls" :key="url">
        <v-img :src="url"></v-img>
      </v-list-item>
    </v-list>
  </div>
</template>
<script lang="ts">
import {
  defineComponent,
  computed,
  ref,
  reactive,
  onMounted
} from "@vue/composition-api";
import Amplify, { Storage } from "aws-amplify";
import { API, graphqlOperation } from "aws-amplify";
import { echo } from "~/src/graphql/queries";
import axios from "axios";
import { Echo } from "../src/API";
import { GraphQLResult } from "@aws-amplify/api";

type URL = string;

type resposnseData = {
  echo: Echo;
};
export default defineComponent({
  setup() {
    const urls = ref<URL[]>([]);
    const message = ref<string>("");
    async function connectLambdaFunc() {
      console.log("start connectiong lambda");
      const response = (await API.graphql({
        query: echo
      })) as GraphQLResult<{ echo: Echo }>;
      // console.log(response);
      let data: any = response.data;
      message.value = data.echo.body;
      let body = JSON.parse(data.echo.body);
      urls.value = body.urls;
    }
    onMounted(() => {
      connectLambdaFunc();
    });
    return { message: message, urls: urls };
  }
});
</script>
