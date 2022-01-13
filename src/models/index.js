// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { Todo, Echo } = initSchema(schema);

export {
  Todo,
  Echo
};