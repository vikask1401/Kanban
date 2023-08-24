const bid = document.currentScript.getAttribute('bid');
const backend = "http://127.0.0.1:5000"

const new_task = Vue.component("new_task", {
    delimiters: ['[[', ']]'],
    props: [
        'listid'
    ],
    data: function () {
        return {
            taskName: "",
            taskDescription: "",
            taskDeadline: ""
        }
    },
    methods: {
        addTask: function () {
            const fd = new FormData()
            fd.append("list_id", this.listid)
            fd.append("task_name", this.taskName)
            fd.append("task_description", this.taskDescription)
            fd.append("task_deadline", this.taskDeadline)
            fetch(backend + "/task", {
                method: "POST",
                body: fd,
                headers: {
                    'Accept': 'application/json',
                },
            })
                .then(response => response.json())
                .then(json => {
                    alert(json.alert)
                    this.$emit("refresh")
                })
        }
    },
    template: `
    <div align='center'>
        <form @submit.prevent="addTask();return false" autocomplete="off" class="form" style="padding-top:0px">
            <p style="color: white;border-bottom: 1px solid white;">
               Add New Task
            </p>
            <label for='tname'>Task Name</label>
            <br>
            <input id='tname' type='text' name="tname" v-model="taskName" required></input>
            <br>
            <br>
            <label for='desc' >Description</label>
            <br>
            <input id='desc' type='text' name="desc" v-model="taskDescription"></input>
            <br>
            <br>
            <label for='dl'>Deadline</label>
            <br>
            <input id='dl' type='date' name="dl" v-model="taskDeadline" required></input>
            <br>
            <br>
            <button @click="$emit('close-new-task-modal')" class="close-btn" style="margin:5px">Close</button>
            <input class="btn" type="submit" value="Add Task">
        </form>
    </div>
    `
}
)

const edit_task = Vue.component("edit_task", {
    delimiters: ['[[', ']]'],
    props: [
        'task'
    ],
    data: function () {
        return {
            taskName: this.task.TaskName,
            taskDescription: this.task.Description,
            taskDeadline: this.task.Deadline
        }
    },
    methods: {
        editTask: function () {
            const fd = new FormData()
            fd.append("task_id", this.task.TaskID)
            fd.append("task_name", this.taskName)
            fd.append("task_description", this.taskDescription)
            fd.append("task_deadline", this.taskDeadline)
            fetch(backend + "/task", {
                method: "PATCH",
                body: fd,
                headers: {
                    'Accept': 'application/json',
                },
            })
            this.task.TaskName = this.taskName
            this.task.Description = this.taskDescription
            this.task.Deadline = this.taskDeadline
            this.task.editMode = false
        }
    },
    template: `
    <div align='center'>
        <form @submit.prevent="editTask();return false" autocomplete="off" class="form" style="padding-top:5px">
            <p style="color:white; border-bottom:1px solid white">Edit [[taskName]]</p>
            <label for='tname'>Task Name</label>
            <br>
            <input id='tname' type='text' name="tname" v-model="taskName" required></input>
            <br>
            <br>
            <label for='desc' >Description</label>
            <br>
            <input id='desc' type='text' name="desc" v-model="taskDescription"></input>
            <br>
            <br>
            <label for='dl'>Deadline</label>
            <br>
            <input id='dl' type='date' name="dl" v-model="taskDeadline" required></input>
            <br>
            <br>
            <button @click="$emit('close-edit-task-modal')" class="close-btn" style="margin:5px">Close</button>
            <input class="btn" type="submit" value="Save Changes">
        </form>
    </div>
    `
}
)

const vm = new Vue({
    el: '#vm',
    delimiters: ['[[', ']]'],
    data: {
        board_data: {},
        addListMode: false,
        listName: ""
    },
    components: {
        new_task
    },
    methods: {
        fetchData() {
            fetch(backend + "/viewboard/" + bid, {
                method: "POST",

            })
                .then((response) => response.json())
                .then((json) => {
                    vm.board_data = json.board_data
                })
        },
        addList() {
            const fd = new FormData()
            fd.append("board_id", bid)
            fd.append("list_name", this.listName)
            fetch(backend + "/list", {
                method: "POST",
                body: fd,
                headers: {
                    'Accept': 'application/json',
                },
            })
                .then(response => response.json())
                .then(json => {
                    this.board_data.push({
                        "id": json.listId,
                        "name": this.listName,
                        "tasks": []
                    })
                    this.listName = ""
                })
        },
        toggleEditList(listId) {
            for (var list of vm.board_data) {
                if (list.id == listId) {
                    Vue.set(list, 'editMode', !list.editMode)
                }
            }
        },
        editList(listId, listName){
            const fd = new FormData()
            fd.append("list_id", listId)
            fd.append("list_name", listName)
            fetch(backend + "/list", {
                method: "PATCH",
                body: fd,
                headers: {
                    'Accept': 'application/json',
                },
            })
        },
        deleteList(listId) {
            const fd = new FormData()
            fd.append("list_id", listId)
            fetch(backend + "/list", {
                method: "DELETE",
                body: fd,
                headers: {
                    'Accept': 'application/json',
                },
            })
                .then(response => response.json())
                .then(json => {
                    deleteList = this.board_data.find(list => list.id === listId)
                    index = this.board_data.indexOf(deleteList)
                    this.board_data.splice(index, 1)
                })
        },
        toggleCreateTask(listId) {
            for (var list of vm.board_data) {
                if (list.id == listId) {
                    Vue.set(list, 'addTaskMode', !list.addTaskMode)
                }
            }
        },
        toggleEditTask(listId, taskId) {

            for (var list of vm.board_data) {
                if (list.id == listId) {
                    for (var task of list.tasks) {
                        if (task.TaskID == taskId) {
                            Vue.set(task, 'editMode', !task.editMode)
                        }
                    }
                }
            }
        },
        startTaskDrag(event, taskId) {
            event.dataTransfer.dropEffect = 'move'
            event.dataTransfer.effectAllowed = 'move'
            event.dataTransfer.setData('taskId', taskId)
        },
        onTaskDrop(event, dropList) {
            const taskId = event.dataTransfer.getData('taskId')
            for (var list of this.board_data) {
                for (var task of list.tasks) {
                    if (task.TaskID == taskId) {
                        const fd = new FormData()
                        fd.append("task_id", task.TaskID)
                        fd.append("list_id", dropList.id)
                        fetch(backend + "/task", {
                            method: "PUT",
                            body: fd,
                            headers: {
                                'Accept': 'application/json',
                            },
                        })
                        index = list.tasks.indexOf(task)
                        dropList.tasks.push(task)
                        list.tasks.splice(index, 1)
                        return
                    }
                }
            }
        },
        deleteTask(taskId) {
            const fd = new FormData()
            fd.append("task_id", taskId)
            fetch(backend + "/task", {
                method: "DELETE",
                body: fd,
                headers: {
                    'Accept': 'application/json',
                },
            })
                .then(response => response.json())
                .then(json => {
                    for (var list of this.board_data) {
                        for (var task of list.tasks) {
                            if (task.TaskID == taskId) {
                                index = list.tasks.indexOf(task)
                                list.tasks.splice(index, 1)
                            }
                        }
                    }
                })
        }
    },
    mounted() {
        this.fetchData()
    }
})


