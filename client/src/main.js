import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from "primevue/config";
import InputText from "primevue/inputtext";
import Panel from 'primevue/panel';
import 'primevue/resources/themes/nova-vue/theme.css';

const app = createApp(App)
app.use(PrimeVue);
app.component('InputText', InputText);
app.component('Panel', Panel);
app.mount('#app')