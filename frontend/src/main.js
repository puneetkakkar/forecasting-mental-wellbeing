import "primeflex/primeflex.css";
import "primevue/resources/themes/lara-light-green/theme.css";
import "primevue/resources/primevue.min.css"; /* Deprecated */
import "primeicons/primeicons.css";
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import FileUpload from 'primevue/fileupload';
import Card from 'primevue/card'
import Button from 'primevue/button'
// import { Chart, registerables } from 'primevue/chart';
import Chart from 'primevue/chart';
import registrables from 'primevue/chart'
import Fieldset from 'primevue/fieldset';
import Dropdown from 'primevue/dropdown';






// createApp(App).use(store).use(router).mount('#app')
const app = createApp(App)

app.use(router).use(PrimeVue, { ripple: true });
app.component('FileUpload', FileUpload);
app.component('Chart', Chart);
app.component('Card', Card);
app.component('Button', Button);
app.component('Fieldset', Fieldset);
app.component('Dropdown', Dropdown);

app.mount('#app');

Chart.register(...registerables);