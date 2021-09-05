<template>
  <div>
    <v-row>
      <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
        <v-form ref="formRef" @submit.prevent="submit">
          <v-text-field label="Name" v-model="formData.name" :rules="requiredRule"></v-text-field>
          <v-textarea label="Description" v-model="formData.description"></v-textarea>
          <v-btn color="primary" class="my-5" large depressed type="submit">Submit</v-btn>
        </v-form>
      </v-col>
      <v-col cols="12" xs="12" sm="12" md="6" lg="6" xl="6">
        <v-list>
          <v-list-item v-for="(item, index) in todos" :key="index">
            <v-list-item-content>
              <v-list-item-title>{{ item.name }}</v-list-item-title>
              <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
            </v-list-item-content>
            <v-btn dark @click="remove(item.id)">削除</v-btn>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  computed,
  ref,
  onMounted
} from "@vue/composition-api";
import { createTodo, deleteTodo } from "~/src/graphql/mutations";
import { API } from "aws-amplify";
import { listTodos } from "~/src/graphql/queries";

type Todo = {
  name: string;
  description?: string;
};

type TodoForDel = {
  id: number;
};

const createTodoDtoDefaults: Todo = Object.freeze({
  name: "",
  description: ""
});

const deleteTodoDtoDefaults: TodoForDel = Object.freeze({
  id: 0
});

export default defineComponent({
  setup() {
    const formData = ref<Todo>({
      ...createTodoDtoDefaults
    });
    const formDataForDel = ref<TodoForDel>({
      ...deleteTodoDtoDefaults
    });
    const todos = ref<Todo[]>([]);

    const formRef = ref();

    const requiredRule = computed(() => [
      (v: string) => !!v || "This field is required"
    ]);

    async function fetchAllTodo() {
      const response = await API.graphql({
        query: listTodos
      });
      // @ts-ignore
      todos.value = response.data.listTodos.items as Todo[];
    }

    async function submit() {
      if (formRef.value.validate()) {
        await API.graphql({
          query: createTodo,
          variables: {
            input: formData.value
          }
        });

        // reset the `formData` values
        formData.value = {
          ...createTodoDtoDefaults
        };
        fetchAllTodo();
      }
    }

    async function remove(id: number) {
      formDataForDel.value.id = id;
      await API.graphql({
        query: deleteTodo,
        variables: {
          input: formDataForDel.value
        }
      });
      formDataForDel.value = {
        ...deleteTodoDtoDefaults
      };
      fetchAllTodo();
    }

    onMounted(() => {
      fetchAllTodo();
    });

    return {
      todos,
      formData,
      formDataForDel,
      formRef,
      submit,
      remove,
      requiredRule
    };
  }
});
</script>
