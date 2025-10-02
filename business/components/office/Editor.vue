<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-2 pb-4">
    <BackButton />
    <ModelForm
      v-if="canEdit || (!defaultData && canView)"
      :title="$t('office_title')"
      :collapsible="true"
      :service="OfficeService"
      :rules="rules"
      :default="defaultData"
      :editable="canEdit"
      contentType="multipart/form-data"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="$t('office_name')" prop="name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.name"
              :placeholder="$t('default_place_holder')"
            />
            <span v-else>{{ scope.current.name }}</span>
          </el-form-item>
          <el-form-item :label="$t('email')" prop="email">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.email"
              :placeholder="$t('default_place_holder')"
            />
            <span v-else>{{ scope.current.email }}</span>
          </el-form-item>
          <el-form-item :label="$t('Address')" prop="address">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.address"
              :placeholder="$t('default_place_holder')"
            />
            <span v-else>{{ scope.current.address }}</span>
          </el-form-item>
          <el-form-item :label="$t('Phone')" prop="phone">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.phone"
              :placeholder="$t('default_place_holder')"
            />
            <span v-else>{{ scope.current.phone }}</span>
          </el-form-item>
          <el-form-item :label="$t('manager')" prop="manager_id">
            <el-select
              v-if="scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.manager_id"
              :placeholder="$t('pick_a_people')"
            >
              <el-option
                v-for="item in employeesStore.allEmployees"
                :key="item.id"
                :label="item.first_name + ' ' + item.last_name"
                :value="item.id"
              />
            </el-select>
            <span v-else>{{
              scope.current.manager.first_name +
              " " +
              scope.current.manager.last_name
            }}</span>
          </el-form-item>
          <el-form-item
            v-loading="isLoading"
            :label="$t('work_sessions')"
            prop="sessions"
          >
            <div
              class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 w-full"
            >
              <el-row v-for="(day, index) in weekDays" :key="index">
                <el-card
                  class="bg-surface max-w-xs md:max-w-sm lg:max-w-md mx-auto min-w-full"
                >
                  <template #header>
                    <div
                      class="flex flex-row h-full bg-primary text-white justify-between align-middle px-2"
                    >
                      <span>{{ day.label }}</span>
                      <div class="flex flex-row">
                        <el-button
                          type="primary"
                          v-if="collapsed"
                          size="small"
                          :icon="CaretBottom"
                          @click="expand()"
                        />
                        <el-button
                          type="primary"
                          v-if="!collapsed"
                          size="small"
                          :icon="CaretTop"
                          @click="collapse()"
                        />
                      </div>
                    </div>
                  </template>
                  <div
                    v-for="(session, index) in sessions"
                    class="flex flex-col gap-2"
                  >
                    <div
                      v-if="session.work_day == day.value"
                      :key="index"
                      class="flex flex-row gap-5 justify-between"
                    >
                      {{ utcToLocalTime(session.start_time, FORMAT.TIME_MINUTE) }} -
                      {{ utcToLocalTime(session.end_time, FORMAT.TIME_MINUTE) }}
                      <span
                        ><el-button
                          type="primary"
                          size="small"
                          :icon="Delete"
                          @click="deleteItem(session.id)"
                        ></el-button
                      ></span>
                    </div>
                  </div>
                  <div class="flex items-center justify-center mt-2">
                    <el-button
                      class="px-5 py-3"
                      type="primary"
                      size="small"
                      :icon="Plus"
                      @click="openDialog(day.value)"
                    ></el-button>
                  </div>
                </el-card>
              </el-row>
            </div>
          </el-form-item>
          <el-form-item :label="$t('employees')">
            <div class="flex flex-col w-full">
              <PaginationTable
                :page-size="5"
                :service="OfficeMembersService"
                :canDeleteItems="canEdit"
                :canEditItems="false"
                :canAddItems="false"
                :multipleSelect="canEdit"
                :allowExportToExcel="true"
                :allowExportToJson="true"
                :searchable="true"
                :disable-row-click="true"
                :reload="isReload"
              >
                <el-table-column
                  prop="first_name"
                  :label="$t('first_name')"
                  min-width="150"
                />
                <el-table-column
                  prop="last_name"
                  :label="$t('last_name')"
                  min-width="150"
                />
                <el-table-column
                  prop="work_mail"
                  :label="$t('work_mail')"
                  min-width="300"
                ></el-table-column>
                <el-table-column
                  prop="date_of_birth"
                  :label="$t('date_of_birth')"
                  min-width="180"
                >
                  <template #default="scope">
                    {{ formatDate(scope.row.date_of_birth) }}
                  </template>
                </el-table-column>
              </PaginationTable>
              <el-select
                v-model="employee_ids"
                multiple
                filterable
                remote
                :reserve-keyword="false"
                :placeholder="$t('work_mail')"
                :remote-method="remoteMethod"
                style="width: auto"
              >
                <el-option
                  v-for="item in options"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
              <el-button
                type="primary"
                :icon="Plus"
                class="self-end px-2 mt-2"
                @click="addMember"
              >
                {{ $t("add_member") }}
              </el-button>
            </div>
          </el-form-item>
        </div>
      </template>
    </ModelForm>
    <span v-else class="text-center">{{ $t("dont_have_permission") }}</span>
    <!-- Add Session Dialog -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle">
      <el-time-picker
        v-model="newSessions.timeRange"
        is-range
        :format="FORMAT.TIME_MINUTE"
        :value-format="FORMAT.TIME"
        :start-placeholder="'Start time'"
        :end-placeholder="'End time'"
      ></el-time-picker>
      <el-row justify="end" style="margin-top: 20px">
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click.prevent="addSessionToDay()"
          >Add</el-button
        >
      </el-row>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { useOauthStore } from "@/stores/oauth";
import { useOfficesStore } from "@/stores/offices";
import { useWorkSessionsStore } from "@/stores/work-session";
import OfficeService from "@/services/offices";
import EmployeeService from "@/services/hrm/employees";
import WorkSessionService from "@/services/hrm/work-sessions";
import { useEmployeesStore } from "@/stores/business/employee";
import OfficeMembersService from "@/services/employee_office_member";
import {
  CaretTop,
  CaretBottom,
  Edit,
  Delete,
  Plus,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { localToUtcTime, utcToLocalTime, FORMAT } from "@/utils/time";
import { ref, watch, computed } from "vue";
const route = useRoute();
// Extract the office_id from the route parameters
const officeId = route.params.id;
const props = defineProps({
  defaultData: {
    type: Object,
    default: null,
  },
});
const sessions = ref<any[]>([]);
const { t } = useI18n();
const collapsed = ref(false);
const isProcessing = ref(false);
const dialogVisible = ref(false);
const oauthStore = useOauthStore();
const employeesStore = useEmployeesStore();
const officesStore = useOfficesStore();
const workSessionStore = useWorkSessionsStore();

const selectedDay = ref("");
const dialogTitle = computed(() => `Add Work Session for ${selectedDay.value}`);
const newSessions = ref({ timeRange: [], work_day: null });
const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["offices:edit"]);
});
const canView = computed(() => {
  return oauthStore.hasOneOfScopes(["offices:view"]);
});

const collapse = () => {
  collapsed.value = true;
};

const expand = () => {
  collapsed.value = false;
};

const openDialog = (workDays: any) => {
  const day = weekDays.find((d) => d.value === workDays);
  selectedDay.value = day?.label || ""; // Set the selected day's label
  newSessions.value.work_day = workDays;
  dialogVisible.value = true;
};

const deleteItem = async (id: any) => {
  try {
    await WorkSessionService.delete(id);
    ElMessage.success("Session deleted successfully!");
    await reloadSessions(); // Reload sessions after deleting
  } catch (error) {
    ElMessage.error("Failed to delete session.");
    console.error("Error deleting session:", error);
  }
};

const addSessionToDay = async () => {
  if (isProcessing.value) return; // Prevent multiple clicks if already processing

  isProcessing.value = true;
  if (newSessions.value.timeRange.length === 2) {
    const session = {
      start_time: localToUtcTime(newSessions.value.timeRange[0]),
      end_time: localToUtcTime(newSessions.value.timeRange[1]),
      work_day: newSessions.value.work_day,
      office_id: officesStore.currentOfficeId,
    };
    if (officeId) {
      try {
        // Attempt to create a new session
        const res = await WorkSessionService.create(session);

        // Log the response and show success message
        ElMessage.success("Session added successfully!");

        // Clear the time range and close the dialog
        newSessions.value.timeRange = [];
        dialogVisible.value = false;
        // Reload sessions after successfully adding the session
        await reloadSessions();
      } catch (error: any) {
        // Handle error response from server
        console.log("err:", error);
        let message = "An unexpected error occurred.";
        if (
          error.response &&
          error.response._data &&
          error.response._data.detail
        ) {
          message = error.response._data.detail[0];
          console.error("Error response:", error.response._data.detail[0]);
        } else if (error.message) {
          // Handle other errors, e.g., network issues
          message = error.message;
          console.error("Error:", error.message);
        }
        // Display error message
        ElMessage.error(`Failed to add session: ${message}`);
      }
    } else {
      console.log("No office id");
      sessions.value.push(session);
    }
  } else {
    ElMessage.warning("Please select a valid time range.");
  }
  isProcessing.value = false;
};
const rules = {
  name: [
    { required: true, message: t("validate_error_required"), trigger: "blur" },
    {
      min: 1,
      max: 50,
      message: t("validate_error_min_max", { min: 1, max: 50 }),
      trigger: "blur",
    },
  ],
  email: [
    { required: true, message: t("validate_error_required"), trigger: "blur" },
    {
      type: "email",
      message: t("validate_error_email_format"),
      trigger: ["blur", "change"],
    },
  ],
  address: [
    {
      min: 1,
      max: 255,
      message: t("validate_error_min_max", { min: 1, max: 255 }),
      trigger: "blur",
    },
  ],
  phone: [
    {
      pattern: /^(?:\+\d{1,2}\s)?\d{10}$/,
      message: t("validate_error_phone_format"),
      trigger: "blur",
    },
  ],
};

onMounted(async () => {
    EmployeeService.fetch();
    WorkSessionService.fetch()
    await officesStore.setCurrentOffice(officeId)
    OfficeService.get(officesStore.currentOfficeId).then((response) => {
        sessions.value = response.sessions
    })

  WorkSessionService.fetch();
  // Ensure scope.current.sessions is in sync with sessions
  if (props.defaultData && props.defaultData.sessions) {
    sessions.value = [...props.defaultData.sessions];
  }
  OfficeMembersService.fetch(true);
});

const list = computed(() => {
  const employees = employeesStore.employees.data;
  const employeesByOffice = employeesStore.employees_by_office.data;

  return employees
    .filter(
      (emp) =>
        !employeesByOffice.some((empByOffice) => empByOffice.id === emp.id)
    )
    .map((item) => {
      return { value: item.id, label: item.work_mail };
    });
});

// Watch for changes in sessions and update props.defaultData.sessions
watch(
  sessions,
  (newSessions) => {
    if (props.defaultData) {
      props.defaultData.sessions = [...newSessions];
    }
  },
  { deep: true }
);

// Watch for changes in props.defaultData.sessions and update sessions
watch(
  () => props.defaultData.sessions,
  (newSessions) => {
    if (newSessions) {
      sessions.value = [...newSessions];
    }
  },
  { deep: true }
);

const reloadSessions = async () => {
  try {
    isLoading.value = true;
    // Assuming you have a method to fetch sessions
    const response = await WorkSessionService.gets();
    sessions.value = response; // Update sessions with the fetched data
  } catch (error) {
    console.error("Error fetching sessions:", error);
  } finally {
    isLoading.value = false;
  }
};

//Sessions:
const weekDays = [
  { value: 0, label: "Monday" },
  { value: 1, label: "Tuesday" },
  { value: 2, label: "Wednesday" },
  { value: 3, label: "Thursday" },
  { value: 4, label: "Friday" },
  { value: 5, label: "Saturday" },
  { value: 6, label: "Sunday" },
];

function formatTime(timeStr) {
  // Assuming timeStr is in 'HH:mm:ss' format
  return timeStr.slice(0, 5); // Extract 'HH:mm' from 'HH:mm:ss'
}

interface ListItem {
  value: string;
  label: string;
}
import PaginationTable from "@/components/PaginationTable.vue";
const options = ref<ListItem[]>([]);
const employee_ids = ref<string[]>([]);
const isLoading = ref(false);
const isReload = ref(false);

const remoteMethod = (query: string) => {
  if (query) {
    setTimeout(() => {
      options.value = list.value.filter((item) => {
        return item.label.toLowerCase().includes(query.toLowerCase());
      });
    }, 200);
  } else {
    options.value = [];
  }
};

const addMember = async () => {
  try {
    await OfficeMembersService.addMember(employee_ids.value);
    employee_ids.value = [];
    isReload.value = true;
    setTimeout(() => {
      isReload.value = false;
    }, 0.5);
    ElMessage.success("Add member successfully");
  } catch (error) {
    console.error(error);
  }
};
</script>
<style scoped>
.work-session-container {
  display: flex;
  flex-direction: row;
  gap: 20px;
  /* Space between rows */
}
</style>
