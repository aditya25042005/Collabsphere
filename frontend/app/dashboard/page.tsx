"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Search, User, Clock } from "lucide-react"
import Navbar from "@/components/navbar"
import { useUserContext } from "@/lib/usercontext"
import Notification from "@/components/notification"
import { API_BASE } from "@/lib/api"

interface Project {
  admin_id: number
  description: string
  project_id: number
  end_date: string
  members_required: number
  current_members?: number
  start_date: string
  status: string
  project_status?: string
  title: string
  tags: string
}

export default function ProjectsPage() {
  const PAGE_SIZE = 10

  const [activeNav, setActiveNav] = useState("dashboard")
  const [searchQuery, setSearchQuery] = useState("")
  const [statusFilter, setStatusFilter] = useState<"all" | "open" | "applied" | "active" | "running" | "completed">("all")
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [loadingMore, setLoadingMore] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const [offset, setOffset] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const sentinelRef = useRef<HTMLDivElement>(null)

  const {user } = useUserContext()
  const userlocal = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
  const parsedUser = userlocal ? JSON.parse(userlocal) : null;
  const userId = user?.id ? user?.id:parsedUser?.id;

  const fetchProjects = useCallback(async (currentOffset: number, replace: boolean) => {
    if (!userId) return;
    replace ? setLoading(true) : setLoadingMore(true)
    try {
      const response = await fetch(`${API_BASE}/list/projects`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, limit: PAGE_SIZE, offset: currentOffset }),
      })
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`)
      const data = await response.json()
      const incoming: Project[] = data.project ?? []
      setProjects(prev => replace ? incoming : [...prev, ...incoming])
      setHasMore(currentOffset + incoming.length < (data.total ?? 0))
      setOffset(currentOffset + incoming.length)
      setError(null)
    } catch (err) {
      console.error("Error fetching projects:", err)
      setError("Failed to load projects. Please try again later.")
    } finally {
      replace ? setLoading(false) : setLoadingMore(false)
    }
  }, [userId])

  // Initial load
  useEffect(() => {
    if (!userId) return;
    setOffset(0)
    setHasMore(true)
    fetchProjects(0, true)
  }, [userId])

  // Infinite scroll via IntersectionObserver
  useEffect(() => {
    if (!sentinelRef.current) return
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loadingMore && !loading) {
          fetchProjects(offset, false)
        }
      },
      { threshold: 0.1 }
    )
    observer.observe(sentinelRef.current)
    return () => observer.disconnect()
  }, [hasMore, loadingMore, loading, offset, fetchProjects])

  // Handle applying to a project
  const handleApplyToProject = async (projectId: number) => {
    try {
      const response = await fetch(`${API_BASE}/apply/project`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          project_id: projectId,
          user_id: userId, 
          role: "member",
          remarks: ""
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }

      const data = await response.json()
      console.log("Apply Response:", data)
      
      // Update the project status in the UI
      setProjects((prevProjects) =>
        prevProjects.map((project) =>
          project.project_id === projectId ? { ...project, status: "Applied" } : project
        )
      )
      
      // Show success message
      alert("Successfully applied to project!")
    } catch (error) {
      console.error("Error applying to project:", error)
      alert("Failed to apply to project. Please try again.")
    }
  }

  // Process tags for each project
  const processedProjects = projects.map(project => {
    // Handle different tag formats: "{tag1,tag2}" or "tag1, tag2" or empty
    let tagArray: string[] = []
    
    if (project.tags) {
      // Remove curly braces if present
      const cleanTags = project.tags.replace(/^\{|\}$/g, '')
      
      if (cleanTags.trim()) {
        // Split by comma and trim each tag
        tagArray = cleanTags.split(/,\s*/).map(tag => tag.trim())
      }
    }
    
    return {
      ...project,
      tagArray
    }
  })

  const matchesStatusFilter = (project: typeof processedProjects[0]) => {
    if (statusFilter === "all") return true
    if (statusFilter === "open") return project.status === "Apply Now"
    if (statusFilter === "applied") return project.status === "Pending" || project.status === "Applied"
    if (statusFilter === "active") return project.status === "Part"
    if (statusFilter === "running")
      return project.status === "Closed" && project.project_status?.toLowerCase() !== "completed"
    if (statusFilter === "completed")
      return project.status === "Closed" && project.project_status?.toLowerCase() === "completed"
    return true
  }

  // Filter projects based on search query + status chip
  const filteredProjects = processedProjects.filter(project => {
    const matchesSearch =
      searchQuery === "" ||
      project.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      project.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      project.tagArray.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))

    return matchesSearch && matchesStatusFilter(project)
  })

  const getProjectStatusInfo = (status: string, projectStatus?: string) => {
    if (status === "Closed") {
      const real = projectStatus?.toLowerCase()
      if (real === "completed") {
        return { displayStatus: "Completed", bgColor: "bg-purple-600 hover:bg-purple-700" }
      }
      return { displayStatus: "Active", bgColor: "bg-blue-500 hover:bg-blue-600" }
    }

    switch (status) {
      case "Apply Now":
        return { displayStatus: "Apply Now", bgColor: "bg-pink-500 hover:bg-pink-600" };
      case "Pending":
        return { displayStatus: "Applied", bgColor: "bg-green-600 hover:bg-green-700" };
      case "Part":
        return { displayStatus: "Participating", bgColor: "bg-blue-500 hover:bg-blue-600" };
      default:
        return { displayStatus: "View Details", bgColor: "bg-blue-600 hover:bg-blue-700" };
    }
  };

  return (
    <div className="flex min-h-screen bg-black text-white">
      {/* Sidebar */}
      <Navbar activeNav={activeNav} setActiveNav={setActiveNav} />
      <div className="fixed top-4 right-6 z-50">
        <Notification />
      </div>
      
      {/* Main content */}
      <div className="flex-1 p-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Explore Projects</h1>
        </div>

        {/* Search Bar */}
        <div className="flex justify-between items-center mb-6">
          <div className="relative w-full max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={18} />
            <Input 
              placeholder="Search projects..." 
              className="pl-10 bg-gray-800 border-gray-700"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>

        {/* Filter chips */}
        <div className="flex items-center gap-2 flex-wrap mb-6">
          {([
            { key: "all",       label: "All",          dot: null,            active: "bg-pink-500 text-white border-pink-500" },
            { key: "open",      label: "Apply Now",    dot: "bg-pink-400",   active: "bg-pink-500/20 text-pink-400 border-pink-500" },
            { key: "applied",   label: "Applied",      dot: "bg-green-400",  active: "bg-green-500/20 text-green-400 border-green-500" },
            { key: "active",    label: "Open Project", dot: "bg-indigo-400", active: "bg-indigo-500/20 text-indigo-400 border-indigo-500" },
            { key: "running",   label: "Active",       dot: "bg-blue-400",   active: "bg-blue-500/20 text-blue-400 border-blue-500" },
            { key: "completed", label: "Completed",    dot: "bg-purple-400", active: "bg-purple-500/20 text-purple-400 border-purple-500" },
          ] as const).map(({ key, label, dot, active }) => {
            const counts: Record<string, number> = {
              all: processedProjects.length,
              open: processedProjects.filter(p => p.status === "Apply Now").length,
              applied: processedProjects.filter(p => ["Pending","Applied"].includes(p.status)).length,
              active: processedProjects.filter(p => p.status === "Part").length,
              running: processedProjects.filter(p => p.status === "Closed" && p.project_status?.toLowerCase() !== "completed").length,
              completed: processedProjects.filter(p => p.status === "Closed" && p.project_status?.toLowerCase() === "completed").length,
            }
            const isActive = statusFilter === key
            return (
              <button
                key={key}
                onClick={() => setStatusFilter(key)}
                className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all ${
                  isActive ? active : "bg-transparent text-gray-400 border-gray-700 hover:border-gray-500"
                }`}
              >
                {dot && <span className={`w-1.5 h-1.5 rounded-full ${dot}`} />}
                {label}
              </button>
            )
          })}
        </div>

        {/* Projects List */}
        {loading ? (
          <div className="text-center py-12">
            <p>Loading projects...</p>
          </div>
        ) : error ? (
          <div className="text-center py-12 text-red-500">
            <p>{error}</p>
            <Button 
              onClick={() => window.location.reload()} 
              className="mt-4 bg-gray-800 hover:bg-gray-700"
            >
              Retry
            </Button>
          </div>
        ) : (
          <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {filteredProjects.map((project) => {
    const statusInfo = getProjectStatusInfo(project.status, project.project_status);
    const isNavigable = project.status === "Part" || project.status === "Closed";
    const cardContent = (
      <Card key={project.project_id} className={`bg-gray-900 border border-gray-800 overflow-hidden hover:border-pink-500/30 transition-all shadow-lg hover:shadow-pink-500/10 h-full flex flex-col ${isNavigable ? "cursor-pointer" : ""}`}>
        <CardHeader className="pb-2 border-b border-gray-800">
          <CardTitle className="text-xl text-white">{project.title}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 py-4 flex-grow">
          <p className="text-gray-300 text-sm line-clamp-3">{project.description}</p>

          <div>
            <p className="text-sm text-gray-400 mb-1">Tech Stack:</p>
            <div className="flex flex-wrap gap-2">
              {project.tagArray.map((tech, index) => (
                <Badge key={index} variant="outline" className="bg-gray-800 text-pink-300 border-pink-500/20 hover:bg-gray-700">
                  {tech}
                </Badge>
              ))}
            </div>
          </div>

          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center">
              <User className="h-4 w-4 mr-1 text-pink-400" />
              <span className="text-gray-300">
                {project.current_members !== undefined
                  ? `${project.current_members}/${project.members_required} members`
                  : `${project.members_required} members`}
              </span>
            </div>
            <div className="flex items-center">
              <Clock className="h-4 w-4 mr-1 text-pink-400" />
              <span className="text-gray-300">Due {new Date(project.end_date).toLocaleDateString()}</span>
            </div>
          </div>
        </CardContent>
        <CardFooter className="bg-gray-800/50 pt-4 border-t border-gray-800">
          {project.status === "Apply Now" ? (
            <Button
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white border-none"
              onClick={(e) => { e.preventDefault(); handleApplyToProject(project.project_id); }}
            >
              Apply Now
            </Button>
          ) : project.status === "Pending" ? (
            <Button className="w-full bg-green-600/80 hover:bg-green-600 text-white" disabled>
              Applied
            </Button>
          ) : project.status === "Part" ? (
            <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
              Open Project
            </Button>
          ) : project.status === "Closed" ? (
            <Button className={`w-full ${statusInfo.displayStatus === "Completed" ? "bg-purple-600 hover:bg-purple-700" : "bg-blue-600 hover:bg-blue-700"} text-white`}>
              {statusInfo.displayStatus}
            </Button>
          ) : (
            <Button className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white">
              View Details
            </Button>
          )}
        </CardFooter>
      </Card>
    );

    return isNavigable ? (
      <Link key={project.project_id} href={`/project/${project.project_id}`}>
        {cardContent}
      </Link>
    ) : (
      <div key={project.project_id}>{cardContent}</div>
    );
  })}
</div>

          {/* Sentinel — triggers next page load when visible */}
          <div ref={sentinelRef} className="h-10" />

          {/* Loading more spinner */}
          {loadingMore && (
            <div className="flex justify-center py-6">
              <div className="w-6 h-6 border-2 border-pink-500 border-t-transparent rounded-full animate-spin" />
            </div>
          )}

          </>
        )}
      </div>
    </div>
  )
}