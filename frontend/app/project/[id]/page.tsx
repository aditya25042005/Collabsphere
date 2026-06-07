"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ProjectDetails from "@/components/project-details"
import SprintManagement from "@/components/sprint-management"
import { useParams } from "next/navigation"
import Navbar from "@/components/navbar"
import ProjectAnalytics from "@/components/project-analytics"

export default function ProjectPage() {
  const params = useParams()
  const projectId = parseInt(params?.id as string)
  const [projectTitle, setProjectTitle] = useState<string>("")
  const [activeNav, setActiveNav] = useState("projects")
  const [projectStatus, setProjectStatus] = useState<string>("")
  const [projectAdminId, setProjectAdminId] = useState<string | number | undefined>(undefined)

  const handleTitleChange = (title: string) => {
    setProjectTitle(title)
    document.title = `${title} | CollabSphere`
  }

  const isProjectClosed = projectStatus?.toLowerCase() === "completed"

  return (
    <div className="flex min-h-screen bg-black text-white">
      <Navbar activeNav={activeNav} setActiveNav={setActiveNav} />

      <div className="flex-1 p-8">
        <div className="flex items-center gap-3 mb-8">
          <h1 className="text-3xl font-bold text-pink-500">
            {projectTitle || "Project Details"}
          </h1>
          {isProjectClosed && (
            <span className="text-xs px-2 py-1 rounded-full bg-zinc-700 text-zinc-300 font-medium">
              Closed
            </span>
          )}
        </div>

        <Tabs defaultValue="details" className="w-full">
          <TabsList className="grid w-full grid-cols-3 bg-zinc-900 mb-8">
            <TabsTrigger value="details" className="data-[state=active]:bg-pink-500">
              Project Details
            </TabsTrigger>
            <TabsTrigger value="sprints" className="data-[state=active]:bg-pink-500">
              Sprint Management
            </TabsTrigger>
            <TabsTrigger value="analytics" className="data-[state=active]:bg-pink-500">
              Project Analytics
            </TabsTrigger>
          </TabsList>

          <TabsContent value="details">
            <ProjectDetails
              project_id={projectId}
              onTitleChange={handleTitleChange}
              onStatusChange={setProjectStatus}
              onAdminIdChange={setProjectAdminId}
            />
          </TabsContent>

          <TabsContent value="sprints">
            <SprintManagement
              project_id={projectId}
              isProjectClosed={isProjectClosed}
            />
          </TabsContent>
          <TabsContent value="analytics">
            <ProjectAnalytics projectId={projectId}/>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}