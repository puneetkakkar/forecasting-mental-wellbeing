<!-- Visualization page for all the graphs -->
<template>
  <div>
    <h1>Visualizations</h1>
    <div>
        <div v-if="dataArray && dataArray.length > 0" class="chart-container">
            <div class="chart-container">
                <div class="card-container">
        <Card class="predict-card">
            <template #title> Worldwide Distribution </template>
            <template #content>
                <p class="m-0">
                    Select a country from drop down to get countries with lesser suicide rates
                </p>
                <p><Dropdown v-model="selectedCountry" editable showClear :options="countryOptions" optionLabel="name" placeholder="Select a Country" @change="onCountryChange" class="w-full md:w-14rem" />
                </p>

                <div v-if="selectedCountry">
                <p>
                    Selected Country: <strong>{{ selectedCountry.name }}</strong>
                </p>

                <Card class="similar-card" v-if="relatedCountries.length > 0">
                    <template #title>Related Countries</template>
                    <template #content>
                      <p>These are the countries with lesser suicide rates</p>
                    <ul>
                        <li v-for="country in relatedCountries" :key="country.country" class="list">
                        <strong>{{ country.country }} :</strong> <strong>{{country.suicide_rate.toFixed(2)}}% </strong>
                        </li>
                    </ul>
                    </template>
                </Card>
                <p v-else>No related countries found.</p>
                </div>

            </template>
       </Card>
   </div>
                <div class="chart-section">
                    <h2 class="chart-title">Predicted Suicide Rate </h2>
                    <Chart type="polarArea" :data="polarChartData" :options="polarChartOptions" class="chart" />
                    </div>

                    <Fieldset legend="Advice" :toggleable="true">
                        <p>
                        The country <strong>{{ maxSuicideCountryName }}</strong> has a predicted suicide rate of <strong>{{ maxPredictedSuicideRate }}</strong>.
                        The government should take suitable actions to improve the current situation.
                        </p>
                    </Fieldset>

                    <div class="chart-section">
                    <h2 class="chart-title">Prevalence by Gender</h2>
                    <Chart type="bar" :data="stackedBarChartData" :options="stackedBarChartOptions" class="chart" />
                    </div>

                    <Fieldset legend="Advice" :toggleable="true">
                    <p>
                        The country with the maximum prevalence between genders is <strong>{{ maxPrevalenceCountryName }}</strong>.
                        It has a prevalence of <strong>{{ maxSuicideRateInMaxPrevalenceCountry }}</strong> % for the gender <strong>{{ maxPrevalenceGender }}</strong>.
                        The government should take suitable actions for this gender category to improve the current situation.
                    </p>
                    </Fieldset>

                    <div class="chart-section age">
                    <h2 class="chart-title">Age Distribution</h2>
                    <Chart type="bar" :data="horizontalBarChartData" :options="horizontalBarChartOptions" class="age chart" />
                    </div>
                    <Fieldset legend="Advice" :toggleable="true">
                        <p>
                            The country <strong>{{ maxAgePercentageInfo.entity }}</strong> has the highest age percentage, with
                            <strong>{{ maxAgePercentageInfo.ageCategory }}</strong> being the most prevalent, accounting for
                            <strong>{{ maxAgePercentageInfo.maxPercentage.toFixed(2) }}%</strong>.
                            The government should take suitable actions to address the age-related issues.
                        </p>
                    </Fieldset>

                    <div class="chart-section">
                    <h2 class="chart-title">Disease Distribution</h2>
                    <Chart type="radar" :data="radarChartData" :options="radarChartOptions" class="chart" />
                    </div>
                </div>  
            </div>    
      <div v-else>
        <p class="no-data-message">No data currently.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js/auto';

export default {
  components: {
    Chart,
  },
  data() {
    return {
      dataArray: null,
      selectedCountry: null,
      countryOptions: [],
      relatedCountries: [],
      polarChartData: {
        labels: [], 
        datasets: [
          {
            label: 'Predicted Suicide Rate',
            backgroundColor: [],
            data: [],
          },
        ],
      },
      stackedBarChartData:{
        labels: [], 
        datasets: [
          {
            label: 'Male',
            data: [], 
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
          },
          {
            label: 'Female',
            data: [], 
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
        ],
      },
      horizontalBarChartData: {
        labels: [], 
        indexAxis: 'y',
        datasets: [
          {
            label: 'Young',
            data: [], 
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
          },
          {
            label: 'Adult',
            data: [], 
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
          {
            label: 'Old',
            data: [], 
            backgroundColor: 'rgba(255, 206, 86, 0.5)',
          },
        ],
      },
      radarChartData: {
        labels: ['Drug Use', 'Eating Disorder', 'Alcohol Use Disorder', 'Bipolar Disorder', 'Anxiety Disorder', 'Schizophrenia', 'Depression'],
        datasets: [],
      },
      radarChartOptions: {
        responsive: true,
        scales: {
          r: {
            beginAtZero: true,
          },
        },
      },
      polarChartOptions: {
        responsive: true,
        scales: {
          x: {
            beginAtZero: true,
          },
          y: {
            beginAtZero: true,
          },
        },
      },
      horizontalBarChartOptions:{
          responsive: true,
          indexAxis: 'y',
          categoryPercentage: 0.5, 
          scales: {
            x: {
              beginAtZero: true,
              stacked: true,
            },
            y: {
              ticks: {
               autoSkip: false,
              },
              stacked: true,
              maxBarThickness: 3
            },
          },
      },
      stackedBarChartOptions: {
        responsive: true,
        scales: {
          x: {
            stacked: true,
            beginAtZero: true,
          },
          y: {
            stacked: true,
            beginAtZero: true,
          },
        },
      },
    };
  },
  watch: {
    selectedCountry(newCountry) {
      this.fetchRelatedCountries(newCountry);
    },
  },
  mounted(){
     this.fetchCountries();
  },
  setup() {
  },
  created() {
    this.getDataArray();
  },
  methods: {
    async fetchCountries(){  
        try {
            const apiUrl = 'http://localhost:5000/api/visual/countries-list'; 
            const response = await fetch(apiUrl, { method: 'GET' });    

            if (response.ok) {
                const result = await response.json();
                this.countryOptions = []

                result?.data?.forEach(country => { 
                    this.countryOptions.push({name: country})
                });
         }
        } catch (error) {
            console.error('Request failed:', error);
        }      
    },
    onCountryChange() {
      return this.countryOptions.filter((country) => country == this.selectedCountry)
    },
    async fetchRelatedCountries(selectedCountry) {
            try {
                const response = await fetch('http://localhost:5000/api/visual/similar-countries', {
                    method: 'POST',
                    body: JSON.stringify({
                        country: selectedCountry.name
                    }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log(result.data);
                    this.relatedCountries = []

                    if (Array.isArray(result.data) && result.data.length > 0) {
                        result?.data?.forEach(item => { 
                            this.relatedCountries.push({
                                country: item.country,
                                suicide_rate: item.suicide_rate
                            })
                        });

                        console.log(this.relatedCountries);
                    }
                    
                }
            } catch (e) {
                console.log(`Request Failed: ${e}`)
            }
    },
    getDataArray() {
      this.dataArray = JSON.parse(this.$route.query.dataArray || '[]');
      this.polarChartData.labels = this.dataArray.map((item) => item.entity);
      this.polarChartData.datasets[0].backgroundColor = this.generateDistinctColors(this.polarChartData.labels.length);
      this.polarChartData.datasets[0].data = this.dataArray.map((item) => item.predictedSuicideRate);

      this.stackedBarChartData.labels = this.dataArray.map((item) => item.entity);
      this.stackedBarChartData.datasets[0].data = this.dataArray.map((item) => item.prevalence_in_males);
      this.stackedBarChartData.datasets[1].data = this.dataArray.map((item) => item.prevalence_in_females);

      this.horizontalBarChartData.labels = this.dataArray.map((item) => item.entity);
      this.horizontalBarChartData.datasets[0].data = this.dataArray.map((item) => item.young_percentage);
      this.horizontalBarChartData.datasets[1].data = this.dataArray.map((item) => item.adult_percentage);
      this.horizontalBarChartData.datasets[2].data = this.dataArray.map((item) => item.old_percentage);

      this.radarChartData.datasets = this.dataArray.map((item) => ({
        label: item.entity,
        data: [item.drug,item.eating,item.alcohol,item.bipolar,item.anxiety,
        item.schizo,
        item.depression],
        backgroundColor: this.generateDistinctColors(this.dataArray.length),
      })
    )},
    generateDistinctColors(count) {
      const colors = [];
      const goldenRatio = 0.618033988749895;
      for (let i = 0; i < count; i++) {
        const hue = (i * goldenRatio) % 1;
        const color = this.hsvToRgb(hue, 0.5, 0.95);
        colors.push(`rgba(${color.r}, ${color.g}, ${color.b}, 0.8)`);
      }
      return colors;
    },
    hsvToRgb(h, s, v) {
      let r, g, b;
      const i = Math.floor(h * 6);
      const f = h * 6 - i;
      const p = v * (1 - s);
      const q = v * (1 - f * s);
      const t = v * (1 - (1 - f) * s);
      switch (i % 6) {
        case 0:
          (r = v), (g = t), (b = p);
          break;
        case 1:
          (r = q), (g = v), (b = p);
          break;
        case 2:
          (r = p), (g = v), (b = t);
          break;
        case 3:
          (r = p), (g = q), (b = v);
          break;
        case 4:
          (r = t), (g = p), (b = v);
          break;
        case 5:
          (r = v), (g = p), (b = q);
          break;
      }
      return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255),
      };
  },
},
computed: {
    maxSuicideCountryName() {
      if (!this.dataArray || this.dataArray.length === 0) return '';
      
      const maxSuicideCountry = this.dataArray.reduce((max, current) =>
        current.predictedSuicideRate > max.predictedSuicideRate ? current : max
      );

      return maxSuicideCountry.entity;
    },

    maxPredictedSuicideRate() {
      if (!this.dataArray || this.dataArray.length === 0) return 0;
      
      const maxPredictedSuicideRate = Math.max(...this.dataArray.map((item) => item.predictedSuicideRate));

      return maxPredictedSuicideRate.toFixed(2);
    },
   maxPrevalenceInfo() {
    if (!this.dataArray || this.dataArray.length === 0) return { entity: '', gender: '', suicideRate: 0 };

    const maxPrevalenceInfo = this.dataArray.reduce((max, current) => {
      const prevalenceRate = Math.max(current.prevalence_in_males, current.prevalence_in_females);
      if (prevalenceRate > max.prevalenceRate) {
        return {
          entity: current.entity,
          gender: current.prevalence_in_males > current.prevalence_in_females ? 'Male' : 'Female',
          suicideRate: current.predictedSuicideRate,
          prevalenceRate,
        };
      } else {
        return max;
      }
    }, { entity: '', gender: '', suicideRate: 0, prevalenceRate: 0 });
    console.log('maxPrevalenceInfo:', maxPrevalenceInfo);
    return maxPrevalenceInfo;
  },
  maxPrevalenceCountryName() {
    return this.maxPrevalenceInfo.entity;
  },
  maxSuicideRateInMaxPrevalenceCountry() {
    return this.maxPrevalenceInfo.prevalenceRate.toFixed(2);
  },
  maxPrevalenceGender() {
    return this.maxPrevalenceInfo.gender;
  },
  maxAgePercentageInfo() {
      if (!this.dataArray || this.dataArray.length === 0) return { entity: '', ageCategory: '', maxPercentage: 0 };

      const maxAgePercentageInfo = this.dataArray.reduce((max, current) => {
        const maxAgePercentage = Math.max(current.young_percentage, current.adult_percentage, current.old_percentage);
        if (maxAgePercentage > max.maxPercentage) {
          let ageCategory;
          if (maxAgePercentage === current.young_percentage) {
            ageCategory = 'Young';
          } else if (maxAgePercentage === current.adult_percentage) {
            ageCategory = 'Adult';
          } else {
            ageCategory = 'Old';
          }

          return {
            entity: current.entity,
            ageCategory,
            maxPercentage: maxAgePercentage,
          };
        } else {
          return max;
        }
      }, { entity: '', ageCategory: '', maxPercentage: 0 });

      return maxAgePercentageInfo;
   },
  },
};
</script>

<style scoped>
.page-title {
  text-align: center;
}
.chart-container{
    display: flex;
    flex-direction: column;
    align-items: center;
    /* flex-wrap: wrap; */
    justify-content: space-around;
    margin-top: 20px;
}
.chart-section {
  width: 100%;
  max-width: 800px;
  margin: 8vh 0 3vh;
}

.chart-title {
  text-align: center;
  margin-bottom: 10px;
}

.chart {
  width: 100%;
  /* width: 70%; */
}

.chart.age{
    height: 100%;
}

.center-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; 
}
.predict-card {
  max-width: 500px;
  text-align: center;
}

.similar-card{
    background: #f9fafbad;
}
.similar-card ul li{
    list-style: none;
    padding: 5px 0px;
}
.similar-card ul{
    display: flex;
    padding: 0;
    margin: 0;
    flex-direction: column;
    align-items: stretch;
    justify-content: center;
}
.list{
    padding: 5px;
}
h1{
    font-size: 2.5rem;
}
.no-data-message{
    font-size: 1.5rem;
}
</style>