"use client"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import TaskForm from "@/components/taskform"
import SprintDetails from "@/components/sprint-details"
import { useUserContext } from "@/lib/usercontext"
import ProjectTasks from "@/components/view_tasks" // Import the updated component
import CreateSprint from "./create_sprint"
import TeamMemberDropdown from "./team-members-dropdown"
import { API_BASE } from "@/lib/api"

interface SprintManagementProps {
  project_id: number;
  projectTitle?: string;
  isProjectClosed?: boolean;
}

interface Sprint {
  End: string,
  Start: string,
  Status: string,
  name: string,
  sprint_id: number,
  id?: number // Add optional id for backward compatibility
}

export default function SprintManagement({ project_id, projectTitle, isProjectClosed = false }: SprintManagementProps) {
  const { user } = useUserContext()
  const [sprints, setSprints] = useState<Sprint[]>([])
  const [selectedSprintId, setSelectedSprintId] = useState<number | undefined>(undefined);
  const [selectedSprint, setSelectedSprint] = useState<Sprint | null>(null)
  const [isCreateSprintOpen, setIsCreateSprintOpen] = useState(false)
  const [isCreateTaskOpen, setIsCreateTaskOpen] = useState(false)

  const fetchSprints = async () => {
    // Fetch sprints from API
   // const response = await fetch(`${API_BASE}/project/view_sprints?project_id=${project_id}`)
   const apiUrl = `${API_BASE}/project/view_sprints?project_id=${project_id}`;

    const response = await fetch(apiUrl, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json()
    setSprints(data.sprints)
    console.log(data)
    
    // If sprints exist and no sprint is selected, select the last sprint by default
    if (data.sprints && data.sprints.length > 0 && !selectedSprintId) {
      const lastSprint = data.sprints[data.sprints.length - 1]
      // Check if sprint_id or id is available (handle both cases)
      const sprintId = lastSprint.sprint_id !== undefined ? lastSprint.sprint_id : lastSprint.id
      setSelectedSprintId(sprintId)
      setSelectedSprint(lastSprint)
    }
  }

  useEffect(() => {
    fetchSprints()
  }, [project_id])

  const handleSprintSelect = (sprint: Sprint) => {
    // Use sprint_id if available, otherwise fall back to id
    const sprintId = sprint.sprint_id !== undefined ? sprint.sprint_id : sprint.id
    setSelectedSprintId(sprintId)
    setSelectedSprint(sprint)
  }

  // Find the selected sprint object
  useEffect(() => {
    if (selectedSprintId && sprints.length > 0) {
      // Look for sprint with matching sprint_id or id
      const sprint = sprints.find(s => 
        (s.sprint_id !== undefined && s.sprint_id === selectedSprintId) ||
        (s.id !== undefined && s.id === selectedSprintId)
      ) || null
      setSelectedSprint(sprint)
    }
  }, [selectedSprintId, sprints])

  return (
    <div className="space-y-4">
      {/* Closed banner */}
      {isProjectClosed && (
        <div className="flex items-center gap-2 px-4 py-2 rounded-md bg-zinc-800 border border-zinc-700 text-zinc-400 text-sm">
          <span className="w-2 h-2 rounded-full bg-zinc-500 inline-block" />
          This project is closed. No new sprints or tasks can be created and task statuses are locked.
        </div>
      )}

      {/* Header + action buttons */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-xl font-bold text-pink-500">
          {projectTitle ? `Sprint Management: ${projectTitle}` : 'Sprint Management'}
        </h1>
        <div className="flex flex-wrap items-center gap-2">
          <Dialog open={isCreateSprintOpen} onOpenChange={setIsCreateSprintOpen}>
            <DialogTrigger asChild>
              <Button
                size="sm"
                disabled={isProjectClosed}
                className="bg-gradient-to-r from-pink-500 to-blue-500 hover:from-pink-600 hover:text-black hover:to-blue-600 disabled:opacity-40"
              >
                Create Sprint
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Sprint</DialogTitle>
              </DialogHeader>
              <CreateSprint
                project_id={project_id}
                onSprintCreated={() => {
                  fetchSprints();
                  setIsCreateSprintOpen(false);
                }}
                onClose={() => setIsCreateSprintOpen(false)}
              />
            </DialogContent>
          </Dialog>

          <Dialog open={isCreateTaskOpen} onOpenChange={setIsCreateTaskOpen}>
            <DialogTrigger asChild>
              <Button
                size="sm"
                className="bg-gradient-to-r from-pink-500 to-blue-500 hover:from-pink-600 hover:text-black hover:to-blue-600 disabled:opacity-40"
                disabled={!selectedSprintId || isProjectClosed}
              >
                Create Task
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add New Task</DialogTitle>
              </DialogHeader>
              <TaskForm
                projectId={project_id}
                onTaskAdded={() => {
                  fetchSprints();
                  setIsCreateTaskOpen(false);
                }}
                sprint_id={selectedSprintId}
              />
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Sprint list — horizontal scroll on mobile, vertical sidebar on desktop */}
      <div className="lg:hidden">
        <p className="text-xs text-muted-foreground mb-2">Select a sprint</p>
        <div className="flex gap-3 overflow-x-auto pb-2 snap-x snap-mandatory">
          {sprints.length > 0 ? sprints.map(sprint => {
            const sprintId = sprint.sprint_id !== undefined ? sprint.sprint_id : sprint.id;
            const isSelected = selectedSprintId === sprintId;
            return (
              <div
                key={sprintId}
                onClick={() => handleSprintSelect(sprint)}
                className={`snap-start flex-shrink-0 w-40 p-3 rounded-lg cursor-pointer border transition-colors ${
                  isSelected
                    ? 'bg-pink-100 border-pink-500 text-black'
                    : 'bg-zinc-900 border-zinc-700 hover:border-pink-400'
                }`}
              >
                <div className="flex items-center justify-between gap-1 mb-1">
                  <span className={`font-medium text-sm truncate ${isSelected ? 'text-black' : ''}`}>{sprint.name}</span>
                  <Badge
                    variant={sprint.Status === "open" ? "default" : "outline"}
                    className={`text-xs shrink-0 ${isSelected ? 'text-black' : ''}`}
                  >
                    {sprint.Status}
                  </Badge>
                </div>
                {sprint.Start && sprint.End && (
                  <p className={`text-xs ${isSelected ? 'text-gray-700' : 'text-muted-foreground'}`}>
                    {new Date(sprint.Start).toLocaleDateString()} –<br />{new Date(sprint.End).toLocaleDateString()}
                  </p>
                )}
              </div>
            );
          }) : (
            <p className="text-muted-foreground text-sm">No sprints yet</p>
          )}
        </div>
      </div>

      {/* Main content — sidebar + details on desktop, stacked on mobile */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {/* Sidebar — hidden on mobile (handled above) */}
        <div className="hidden lg:block lg:col-span-1">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Project Sprints</CardTitle>
              <CardDescription className="text-xs">Select a sprint to view details</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 max-h-[65vh] overflow-y-auto pr-1">
              {sprints.length > 0 ? (
                sprints.map(sprint => {
                  const sprintId = sprint.sprint_id !== undefined ? sprint.sprint_id : sprint.id;
                  const isSelected = selectedSprintId === sprintId;
                  return (
                    <div
                      key={sprintId}
                      onClick={() => handleSprintSelect(sprint)}
                      className={`p-3 rounded-md cursor-pointer transition-colors ${
                        isSelected
                          ? 'bg-pink-100 border-l-4 border-pink-500 text-black'
                          : 'hover:bg-gray-100 hover:text-black'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1">
                        <h3 className={`font-medium text-sm truncate ${isSelected ? 'text-black' : ''}`}>
                          {sprint.name}
                        </h3>
                        <Badge
                          variant={sprint.Status === "open" ? "default" : "outline"}
                          className={`text-xs shrink-0 ${isSelected ? 'text-black' : ''}`}
                        >
                          {sprint.Status}
                        </Badge>
                      </div>
                      {sprint.Start && sprint.End && (
                        <p className={`text-xs mt-1 ${isSelected ? 'text-gray-700' : 'text-muted-foreground'}`}>
                          {new Date(sprint.Start).toLocaleDateString()} – {new Date(sprint.End).toLocaleDateString()}
                        </p>
                      )}
                    </div>
                  );
                })
              ) : (
                <p className="text-muted-foreground text-sm">No sprints available</p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Details and tasks */}
        <div className="lg:col-span-3 space-y-4">
          {selectedSprint ? (
            <>
              <SprintDetails sprint={selectedSprint} />
              <ProjectTasks
                projectId={project_id}
                sprint_id={selectedSprintId}
                isProjectClosed={isProjectClosed}
              />
            </>
          ) : (
            <div className="text-center py-12 bg-gray-50 rounded-lg border border-dashed border-gray-300">
              <h3 className="text-lg font-medium text-gray-700 mb-2">No Sprint Selected</h3>
              <p className="text-gray-500 mb-4">Select a sprint from the list or create a new one</p>
              <Button
                onClick={() => setIsCreateSprintOpen(true)}
                className="bg-gradient-to-r from-pink-500 to-blue-500 hover:from-pink-600 hover:to-blue-600"
              >
                Create First Sprint
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}