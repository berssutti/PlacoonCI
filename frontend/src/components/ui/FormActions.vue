<template>
    <v-row>
        <v-col cols="12" class="text-right">
            <v-btn color="grey" class="mr-2" @click="$emit('cancel')">Cancelar</v-btn>
            <v-btn type="submit" color="primary" @click="$emit('save')">Salvar</v-btn>
        </v-col>
    </v-row>
</template>

<script setup>
defineEmits(['cancel', 'save']);
</script>
