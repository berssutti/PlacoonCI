<template>
  <v-card-text>
    <h3 class="section-title"><v-icon class="mr-1">mdi-file-document-multiple-outline</v-icon>Informações Gerais</h3>
    <v-row>
      <v-col cols="12" md="6">
        <strong>Nome:</strong> {{ project.name }}
      </v-col>
      <v-col cols="12" md="6">
        <strong>Descrição:</strong> {{ project.description }}
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <strong>Processo SEI:</strong> {{ project.processo_sei }}
      </v-col>
      <v-col cols="12" md="6">
        <strong>Status:</strong> {{ project.status || 'N/A' }}
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <strong>Data de Início:</strong> {{ formatDate(project.start_date) }}
      </v-col>
      <v-col cols="12" md="6">
        <strong>Data de Término:</strong> {{ formatDate(project.end_date) }}
      </v-col>
    </v-row>

    <h3 class="section-title"><v-icon class="mr-1">mdi-account-tie</v-icon>Gestão</h3>
    <v-row>
      <v-col cols="12" md="6">
        <strong>Coordenador:</strong> {{ project.coordinator }}
      </v-col>
      <v-col cols="12" md="6">
        <strong>Coordenador Substituto:</strong> {{ project.substitute_coordinator }}
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <strong>Supervisor Acadêmico:</strong> {{ project.academic_supervisor }}
      </v-col>
    </v-row>

    <template v-if="project.status === 'Recebido'">
      <h3 class="section-title"><v-icon class="mr-1">mdi-note-text-outline</v-icon>Célula Orçamentária</h3>
      <v-row>
        <v-col cols="12" md="4">
          <strong>Nota de Dotação:</strong> {{ project.nota_dotacao }}
        </v-col>
        <v-col cols="12" md="4">
          <strong>PTRES:</strong> {{ project.ptres }}
        </v-col>
        <v-col cols="12" md="4">
          <strong>UGR:</strong> {{ project.ugr }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <strong>Fonte de Recurso:</strong> {{ project.funding_source }}
        </v-col>
        <v-col cols="12" md="6">
          <strong>Natureza Detalhada:</strong> {{ project.detailed_nature }}
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <strong>Plano Interno:</strong> {{ project.internal_plan }}
        </v-col>
        <v-col cols="12" md="6">
          <strong>Nome do Plano Interno:</strong> {{ project.internal_plan_name }}
        </v-col>
      </v-row>
    </template>

    <h3 class="section-title"><v-icon class="mr-1">mdi-cash-multiple</v-icon>Orçamento</h3>
    <v-row>
      <v-col cols="12" md="6">
        <strong>Custos Indiretos UnB:</strong> R$ {{ formatNumber(project.total_unb_amount_expected) }}
      </v-col>
      <v-col cols="12" md="6">
        <strong>Custos Indiretos FCTE:</strong> R$ {{ formatNumber(project.total_fcte_amount_expected) }}
      </v-col>
    </v-row>

    <h3 class="section-title"><v-icon class="mr-1">mdi-shape-outline</v-icon>Áreas</h3>
    <v-row>
      <v-col cols="12">
        <v-chip
          v-for="(area, index) in project.areas"
          :key="index"
          class="ma-1"
          color="primary"
        >
          {{ area.area_name }} - {{ area.percentage }}%
        </v-chip>
      </v-col>
    </v-row>
  </v-card-text>
</template>

<script>
export default {
  name: 'ProjectInfo',
  props: {
    project: {
      type: Object,
      required: true
    },
    formatDate: {
      type: Function,
      required: true
    },
    formatNumber: {
      type: Function,
      required: true
    }
  },
  setup(props) {
    return {
      project: props.project,
      formatDate: props.formatDate,
      formatNumber: props.formatNumber,
    };
  }
};
</script>

<style scoped>
.section-title {
  font-size: 1.1em;
  font-weight: bold;
  margin-top: 16px;
  margin-bottom: 8px;
  border-bottom: 2px solid #eeeeee;
  padding-bottom: 4px;
}

.v-chip {
  margin: 4px;
}

.v-row {
  margin-bottom: 8px;
}
</style>
