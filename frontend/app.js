const API_URL = "http://127.0.0.1:8000";

const taskList = document.getElementById("taskList");
const message = document.getElementById("message");

const totalTasks = document.getElementById("totalTasks");
const todoTasks = document.getElementById("todoTasks");
const progressTasks = document.getElementById("progressTasks");
const completedTasks = document.getElementById("completedTasks");

const taskTitle = document.getElementById("taskTitle");
const priority = document.getElementById("priority");
const status = document.getElementById("status");
const projectId = document.getElementById("projectId");

const addTaskBtn = document.getElementById("addTaskBtn");
const refreshBtn = document.getElementById("refreshBtn");
const quickAddInput = document.getElementById("quickAddInput");
const quickAddBtn = document.getElementById("quickAddBtn");
const searchTitle = document.getElementById("searchTitle");
const searchBtn = document.getElementById("searchBtn");
const sortPriorityBtn = document.getElementById("sortPriorityBtn");
const showAllBtn = document.getElementById("showAllBtn");

async function quickAddTask() {
    const text = quickAddInput.value.trim();

    if (!text) {
        message.textContent = "Please describe the task.";
        return;
    }

    try {
        message.textContent = "✨ AI is creating your task...";
        quickAddBtn.disabled = true;

        const aiResponse = await fetch(
            `${API_URL}/tasks/quick-add`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text
                })
            }
        );

        const aiTask = await aiResponse.json();

        if (!aiResponse.ok) {
            throw new Error(
                aiTask.detail || "AI Quick Add failed"
            );
        }

        const project = Number(projectId.value);

        if (!project) {
            message.textContent =
                "AI understood the task, but Project ID is required to save it.";
            return;
        }

        const createResponse = await fetch(
            `${API_URL}/tasks`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: aiTask.title,
                    priority: aiTask.priority,
                    status: "todo",
                    project_id: project
                })
            }
        );

        const createdTask = await createResponse.json();

        if (!createResponse.ok) {
            throw new Error(
                createdTask.detail || "Task creation failed"
            );
        }

        quickAddInput.value = "";

        message.textContent =
            "✨ AI task created successfully.";

        await loadTasks();

    } catch (error) {
        console.error(error);
        message.textContent = error.message;
    } finally {
        quickAddBtn.disabled = false;
    }
}function displayTasks(tasks) {

    if (tasks.length === 0) {
        taskList.innerHTML = `
            <p class="empty">No tasks found.</p>
        `;
        return;
    }

    taskList.innerHTML = tasks.map(task => `
        <div class="task-card">

            <div>
                <div class="task-title">
                    ${escapeHtml(task.title)}
                </div>

                <div class="task-meta">
                    Status: ${formatStatus(task.status)}
                    • Project: ${task.project_id}
                </div>
            </div>

            <div>
                <span class="badge badge-${task.priority}">
                    ${task.priority}
                </span>

                <button onclick="updateTask(${task.id})">
                    Update
                </button>

                <button onclick="deleteTask(${task.id})">
                    Delete
                </button>
            </div>

        </div>
    `).join("");
}


function updateStats(tasks) {

    totalTasks.textContent = tasks.length;

    todoTasks.textContent =
        tasks.filter(task => task.status === "todo").length;

    progressTasks.textContent =
        tasks.filter(task => task.status === "in_progress").length;

    completedTasks.textContent =
        tasks.filter(task => task.status === "completed").length;
}


async function createTask() {

    const title = taskTitle.value.trim();
    const selectedPriority = priority.value;
    const selectedStatus = status.value;
    const selectedProjectId = Number(projectId.value);

    if (!title) {
        message.textContent = "Please enter a task title.";
        return;
    }

    if (!selectedProjectId) {
        message.textContent = "Please enter a Project ID.";
        return;
    }

    try {

        message.textContent = "Creating task...";

        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: title,
                priority: selectedPriority,
                status: selectedStatus,
                project_id: selectedProjectId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Task creation failed");
        }

        taskTitle.value = "";
        projectId.value = "";

        message.textContent = "Task created successfully.";

        await loadTasks();

    } catch (error) {
        console.error(error);
        message.textContent = error.message;
    }
}


async function updateTask(taskId) {

    const newTitle = prompt("Enter new task title:");

    if (newTitle === null) {
        return;
    }

    const title = newTitle.trim();

    if (!title) {
        alert("Task title cannot be blank.");
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/tasks/${taskId}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    title: title
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Task update failed");
        }

        message.textContent = "Task updated successfully.";

        await loadTasks();

    } catch (error) {
        console.error(error);
        message.textContent = error.message;
    }
}


async function deleteTask(taskId) {

    const confirmed = confirm(
        "Are you sure you want to delete this task?"
    );

    if (!confirmed) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/tasks/${taskId}`,
            {
                method: "DELETE"
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Task deletion failed");
        }

        message.textContent = "Task deleted successfully.";

        await loadTasks();

    } catch (error) {
        console.error(error);
        message.textContent = error.message;
    }
}


function formatStatus(status) {

    if (status === "in_progress") {
        return "In Progress";
    }

    if (status === "completed") {
        return "Completed";
    }

    return "To Do";
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}


addTaskBtn.addEventListener("click", createTask);

refreshBtn.addEventListener("click", loadTasks);

loadTasks();
async function searchTasks() {
    const title = searchTitle.value.trim();

    if (!title) {
        message.textContent = "Please enter a task title.";
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/tasks/search?title=${encodeURIComponent(title)}&algo=binary`
        );

        const task = await response.json();

        if (!response.ok) {
            throw new Error(task.detail || "Task not found");
        }

        displayTasks([task]);
        message.textContent = "Task found using Binary Search.";

    } catch (error) {
        taskList.innerHTML = `
            <p class="empty">Task not found.</p>
        `;

        message.textContent = error.message;
    }
}


async function sortByPriority() {
    try {
        const response = await fetch(
            `${API_URL}/tasks?sort=priority`
        );

        if (!response.ok) {
            throw new Error("Unable to sort tasks.");
        }

        const tasks = await response.json();

        displayTasks(tasks);
        message.textContent = "Tasks sorted by priority.";

    } catch (error) {
        message.textContent = error.message;
    }
}


searchBtn.addEventListener("click", searchTasks);

sortPriorityBtn.addEventListener("click", sortByPriority);

showAllBtn.addEventListener("click", loadTasks);
quickAddBtn.addEventListener("click", quickAddTask);