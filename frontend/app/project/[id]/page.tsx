"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ProjectDetails from "@/components/project-details"
import SprintManagement from "@/components/sprint-management"
import { useParams } from "next/navigation"
import Navbar from "@/components/navbar"
import ProjectAnalytics from "@/components/project-analytics"
import {API_BASE} from "../../../components/api"

export default function ProjectPage() {
  const params = useParams()
  const projectId = parseInt(params?.id as string)
  const [projectTitle, setProjectTitle] = useState<string>("")
  const [activeNav, setActiveNav] = useState("projects")
  
  // This function will be passed to ProjectDetails component
  const handleTitleChange = (title: string) => {
    console.log("Project title received:", title)
    setProjectTitle(title)
    // Optionally update document title
    document.title = `${title} | CollabSphere`
  }
  
  return (
    <div className="flex min-h-screen bg-black text-white">
      <Navbar activeNav={activeNav} setActiveNav={setActiveNav} />
      
      <div className="flex-1 p-8">
        <h1 className="text-3xl font-bold text-pink-500 mb-8">
          {projectTitle || "Project Details"}
        </h1>
        
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
            />
          </TabsContent>
          
          <TabsContent value="sprints">
            <SprintManagement 
              project_id={projectId}
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