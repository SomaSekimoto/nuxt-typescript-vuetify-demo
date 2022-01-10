<template>
  <div>
    <h1>Images</h1>
    <v-list>
      <v-list-item></v-list-item>
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
import fetchS3Files from "~/src/graphql/queries";
export default defineComponent({
  setup() {
    async function connectLambdaFunc() {
      console.log("start connectiong lambda");
      const response = await API.graphql({
        query: fetchS3Files
      });
      console.log(response);
    }
    onMounted(() => {
      connectLambdaFunc();
    });
  }
});
</script>
