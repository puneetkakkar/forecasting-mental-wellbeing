<!-- Input page to upload an excel with data and download template. -->
<template>
  <div class="input">
    <h2>Input a csv file</h2>
    <div class="file-upload-container">
      <FileUpload name="demo[]" url="http://localhost/api/v1/predict/rf" @upload="onAdvancedUpload($event)" :multiple="false" accept=".csv" :maxFileSize="1000000" class="custom">
        <template #empty>
          <p>Drag and drop files here to upload.</p>
        </template>
      </FileUpload>
    </div>
   <div class="template"> 
    <h2> Download template CSV </h2>
    <Button label="Download" icon="pi pi-download" @click="downloadTemplate" severity="success"/>
   </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      code: null,
      entity: null,
      predictedSuicideRate: null,
      prevalence_in_males: null,
      prevalence_in_females: null,
      adult_percentage: null,
      young_percentage: null,
      old_percentage: null,
      drug: null,
      anxiety: null,
      bipolar: null,
      alcohol: null,
      schizo: null,
      eating: null,
      depression: null
    };
  },
  methods: {
    async onAdvancedUpload(event) {
      const formData = new FormData();
      formData.append('file', event.files[0]);

      try {
        const response = await fetch('http://localhost:5000/api/predict/rf', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          if (Array.isArray(result.data) && result.data.length > 0) {
            const dataArr = result.data.map(item => ({
              code: item.code,
              entity: item.entity,
              predictedSuicideRate: item.predicted_suicide_rate,
              prevalence_in_males: item.prevalence_in_males,
              prevalence_in_females: item.prevalence_in_females,
              young_percentage: item.young_percentage ,
              adult_percentage: item.adult_percentage ,
              old_percentage: item.old_percentage ,
              drug: item.drug_use_disorders,
              anxiety: item.anxiety_disorders,
              bipolar: item.bipolar_disorder,
              alcohol: item.alcohol_use_disorders,
              schizo: item.schizophrenia,
              eating: item.eating_disorders,
              depression: item.depression
            }));
          
           console.log('Data Array:', dataArr);

            this.$router.push({
              name: 'Visualize',
              query: {
                dataArray: JSON.stringify(dataArr),
              },
           });

          console.log('API Response:', result);
        } else {
          console.error('API Error:', response.statusText);
        }
       }
      } catch (error) {
        console.error('Request failed:', error);
      }
    },
    downloadTemplate() {
      const templatePath = '/template.csv'; 
      const link = document.createElement('a');
      link.href = templatePath;
      link.download = 'template.csv';
      link.click();
    },
  },
};
</script>

<style scoped>
h2{
  font-size: 1.9rem;
}
.file-upload-container {
  padding: 20px;
  text-align: center;
  display: flex;
  justify-content: center;

  align-items: center;
  margin-bottom: 60px;
}


.custom .p-fileupload-choose{
  background-color: #42b983; 
  color: white; 
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;   

}

.p-fileupload-choose input,
.custom .p-fileupload-upload{
  background-color: #42b983; 
  color: white; 
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;   
}
.custom .p-fileupload-cancel {
  background-color: #42b983; 
  color: white; 
  padding: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.p-fileupload-upload,
.custom .p-fileupload-cancel {
  background-color: #45a049; 
}

.custom .p-fileupload-dragdrop-highlight {
  border-color: #45a049; 
}

.template {
  padding: 20px;
  margin-top: 20px;
  text-align: center;
}

.template button {
  background-color: #4993f5; 
  color: white;
  padding: 15px;
  font: 1.1em;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}
</style>