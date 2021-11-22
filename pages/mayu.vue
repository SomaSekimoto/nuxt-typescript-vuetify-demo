<template>
  <div>
    <p>松岡茉優</p>
    <v-list v-if="reactiveData.media.length">
      <v-list-item v-for=" (obj,i) in reactiveData.media" :key="i">
        <template v-if="obj.key != ''">
          <v-list-item-content>
            <v-list-item-title>{{obj.key}}</v-list-item-title>
            <template v-if="obj.url && obj.url.match(/\.(mp4)/)">
              <video :src="obj.url" controls />
            </template>
            <template v-else>
              <img :src="obj.url" />
            </template>
          </v-list-item-content>
        </template>
      </v-list-item>
    </v-list>
    <!-- <p>{{reactiveData.presignedUrl}}</p> -->
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
// import aws_mobile from "../src/aws-exports";
// Amplify.configure({
//   Auth: {
//     identityPoolId: aws_mobile.aws_cognito_identity_pool_id, //REQUIRED - Amazon Cognito Identity Pool ID
//     region: aws_mobile.aws_cognito_region, // REQUIRED - Amazon Cognito Region
//     userPoolId: aws_mobile.aws_user_pools_id, //OPTIONAL - Amazon Cognito User Pool ID
//     userPoolWebClientId: aws_mobile.aws_user_pools_web_client_id //OPTIONAL - Amazon Cognito Web Client ID
//   },
//   Storage: {
//     bucket: aws_mobile.aws_user_files_s3_bucket, //REQUIRED -  Amazon S3 bucket
//     region: aws_mobile.aws_user_files_s3_bucket_region //REQUIRED -  bucket region
//   }
// });
export default defineComponent({
  setup() {
    const reactiveData = reactive<{
      presignedUrl: string;
      media: Array<any>;
      // media: { key: string }[];
      // media: any;
    }>({ presignedUrl: "", media: [] });

    async function getPresignedUrl(s3Key: string) {
      console.log(s3Key);
      let presignedUrl: string = "";
      await Storage.get(s3Key)
        .then(result => {
          presignedUrl = result;
        })
        .catch(err => console.log(err));
      console.log(presignedUrl);
      return presignedUrl;
    }

    async function getPresignedUrls() {
      await Storage.list("", { level: "public" })
        .then(async result => {
          reactiveData.media = result;
          // reactiveData.presignedUrl = "aa";
          reactiveData.media = await Promise.all(
            reactiveData.media.map(async m => {
              m.url = await getPresignedUrl(m.key);
              return m;
            })
          );
          console.log("media");
          console.log(reactiveData.media);
        })
        .catch(async err => console.log(err));
    }

    onMounted(() => {
      getPresignedUrls();
    });

    return { reactiveData };
  }
});
</script>
