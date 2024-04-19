<template>
<div>
<Stepper>
    <StepperPanel >
        <template #header="{ index, clickCallback }">
            <div class="header-container">
                <button class="custom-button" @click="updateActive(index); clickCallback();">
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    1
                </span>
                </button>
                <div style="font-weight: bold; padding: 0.5em;">Datasets</div>
                <Dropdown :options="options" v-model="selectedOption" placeholder="选择一个选项" />
            </div>
        </template>
        <template #content="{ index, nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto;" @click="NextCallback(index,nextCallback)" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel >
        <template #header="{ index, clickCallback }">
            <div class="header-container">
                <button class="custom-button" @click="updateActive(index); clickCallback();">
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    2
                </span>
                </button>
                <div style="font-weight: bold; padding: 0.5em;">Model</div>
                <Dropdown :options="options" v-model="selectedOption" placeholder="选择一个选项" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right"  style="margin-left:auto;" @click="NextCallback(index, nextCallback)" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel>
        <template #header="{ index, clickCallback }">
            <div class="header-container">
                <button class="custom-button" @click="updateActive(index); clickCallback();">
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    3
                </span>
                </button>
                <div style="font-weight: bold; padding: 0.5em;">Tag</div>
                <Dropdown :options="options" v-model="selectedOption" placeholder="选择一个选项" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }" >
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto;" @click="NextCallback(index, nextCallback)" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel>
        <template #header="{ index, clickCallback }">
            <div class="header-container">
                <button class="custom-button" @click="updateActive(index); clickCallback();">
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    4
                </span>
                </button>
                <div style="font-weight: bold; padding: 0.5em;">Category</div>
                <Dropdown :options="options" v-model="selectedOption" placeholder="选择一个选项" />
            </div>
        </template>
        <template #content="{ index, prevCallback, nextCallback }" >
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Next" icon="pi pi-arrow-right" iconPos="right" style="margin-left:auto;" @click="NextCallback(index, nextCallback)" />
            </div>
        </template>
    </StepperPanel>
    <StepperPanel >
        <template #header="{ index, clickCallback }">
            <div class="header-container">
                <button class="custom-button" @click="updateActive(index); clickCallback();">
                <span :class="['step-indicator', { 'active': index < active, 'inactive': index >= active }]">
                    5
                </span>
                </button>
                <div style="font-weight: bold; padding: 0.5em;">Standard</div>
                <Dropdown :options="options" v-model="selectedOption" placeholder="选择一个选项" />
            </div>
        </template>
        <template #content="{ index, prevCallback }">
            <div class="flex pt-4 justify-content-end" style="display: flex;">
                <Button label="Back" severity="secondary" icon="pi pi-arrow-left" style="margin-right:auto; display: block;" @click="PrevCallback(index, prevCallback)" />
                <Button label="Submit" v-if="canSubmit" icon="pi pi-check" iconPos="right" style="background-color: limegreen;border-color: aliceblue;margin-left:auto"   @click="submitData" />
            </div>
        </template>
    </StepperPanel>
</Stepper>
</div>
</template>

<script>

import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';

export default {
  name: 'App',
  components: {
    Stepper,
    StepperPanel,
    Button,
    Dropdown
  },
  data() {
    return {
      selectedOption: null,
      options: [
        { label: '选项1', value: '1' },
        { label: '选项2', value: '2' },
        { label: '选项3', value: '3' }
      ],
      active: 0,
      canSubmit: false,
      stepLength: 5,
    };
  },
  methods: {
    updateActive(index) {
        this.active = index;
        console.log("active", this.active);
        if(this.active == this.stepLength-1) {
            this.canSubmit = true;
        }
    },
    NextCallback(index, nextCallback) {
        this.active = index +1;
        console.log("active", this.active);
        if(this.active == this.stepLength-1) {
            this.canSubmit = true;
        }
        nextCallback();
    },
    PrevCallback(index, prevCallback) {
        this.active = index - 1;
        console.log("active", this.active);
        prevCallback();
    },
    submitData() {
        console.log("submit");
        this.canSubmit = false;
        this.$store.dispatch("updateSelectSubmitted", true);
    }
  }
}
</script>

<style>
.header-container {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center align items vertically in the container */
}

.custom-button {
  background: transparent;
  border: none;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.step-indicator {
  border-radius: 50%; /* Makes the border rounded */
  border: 2px solid;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgb(241, 248, 250);
}

.active {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.inactive {
  border-color: var(--surface-border-color);
}

/* Define custom CSS variables for colors */
:root {
  --primary-color: #4a97ea; /* Blue, example */
  --surface-border-color: #ccc; /* Grey, example */
}
</style>

<style scoped>
.stepper-line {
  transform: translateY(10px);
}
::v-deep .p-stepper-header {
    align-items: flex-start !important;
}
::v-deep .p-stepper-separator {
    margin-top: 20px;
    height: 3px !important;
}
</style>
