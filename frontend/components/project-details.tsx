
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Calendar, Clock, Users, Briefcase, Code, Flag, Github, ArrowLeft, Star } from "lucide-react"
import Link from "next/link"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { useEffect, useState } from "react"
import { useUserContext } from "@/lib/usercontext"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import { toast } from "sonner"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
  DialogFooter,
  DialogDescription,
} from "@/components/ui/dialog"
import { Slider } from "@/components/ui/slider" // Import Slider for rating
import { API_BASE } from "@/lib/api"

// Update interface to match the actual API response
interface ProjectDetails {
  description: string
  end_date: string
  github_link: string
  project_size: number
  project_type: string
  start_date: string
  team_members: string[]
  tech_stack: string
  title: string
  status?: "planning" | "running" | "completed"
  rating?: number | null
  rating_count?: number
  is_member?: boolean
  has_rated?: boolean
  admin_id?: string | number
}

interface ProjectDetailsProps {
  project_id: number;
  onTitleChange?: (title: string) => void;
  onStatusChange?: (status: string) => void;
  onAdminIdChange?: (adminId: string | number) => void;
}

const fetchProjectDetails = async(project_id: number, userId?: string) => {
  try {
    const url = userId
      ? `${API_BASE}/project/view_details?project_id=${project_id}&user_id=${userId}`
      : `${API_BASE}/project/view_details?project_id=${project_id}`;
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      console.log("Error:", response.status);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    console.log("API Response:", data);
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

// Function to update project status
const updateProjectStatus = async (project_id: number, newStatus: string, userId: string) => {
  try {
    const response = await fetch(`${API_BASE}/project/update_status`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        project_id,
        user_id: userId,
        status: newStatus
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error updating project status:", error);
    throw error;
  }
}

// New function to submit project rating
const submitProjectRating = async (project_id: number, userId: string, rating: number) => {
  const response = await fetch(`${API_BASE}/rate_project`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      project_id,
      user_id: userId,
      score: rating,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Request failed (${response.status})`);
  }
  return data;
}

interface ProjectRating {
  score: number;
  comment: string | null;
  reviewer_name: string;
}

export default function ProjectDetails({ project_id, onTitleChange, onStatusChange, onAdminIdChange }: ProjectDetailsProps) {
  const [projectDetails, setProjectDetails] = useState<ProjectDetails>();
  const [loading, setLoading] = useState(true);
  const [statusUpdating, setStatusUpdating] = useState(false);
  const [ratingValue, setRatingValue] = useState<number>(5);
  const [ratingComment, setRatingComment] = useState<string>("");
  const [isRatingDialogOpen, setIsRatingDialogOpen] = useState(false);
  const [isSubmittingRating, setIsSubmittingRating] = useState(false);
  const [projectRatings, setProjectRatings] = useState<ProjectRating[]>([]);

  const { user } = useUserContext();
  
  // Get user ID from context or local storage
  const userlocal = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
  const parsedUser = userlocal ? JSON.parse(userlocal) : null;
  const userId = user?.id ? user.id : parsedUser?.id;
 
  const fetchRatings = async () => {
    try {
      const res = await fetch(`${API_BASE}/project/ratings?project_id=${project_id}`, {
        credentials: "include",
      });
      if (res.ok) {
        const data = await res.json();
        setProjectRatings(data.ratings ?? []);
      }
    } catch (e) {
      console.error("Error fetching ratings:", e);
    }
  };

  useEffect(() => {
    const getProjectDetails = async () => {
      setLoading(true);
      const details = await fetchProjectDetails(project_id, userId);
      if (details) {
        setProjectDetails({
          ...details,
          status: details.status || "planning",
        });

        if (onTitleChange && details.title) onTitleChange(details.title);
        if (onStatusChange && details.status) onStatusChange(details.status);
        if (onAdminIdChange && details.admin_id) onAdminIdChange(details.admin_id);
      }
      setLoading(false);
    };

    getProjectDetails();
    fetchRatings();
  }, [project_id, userId]);
  
  // Handle status change
  const handleStatusChange = async (newStatus: "planning" | "running" | "completed") => {
    if (!userId) {
      toast.error("You need to be logged in to change project status");
      return;
    }
    try {
      setStatusUpdating(true);
      const response = await fetch(`${API_BASE}/project/update_status`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id, user_id: userId, status: newStatus }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Failed to update status");
      setProjectDetails(prev => prev ? { ...prev, status: newStatus } : prev);
      if (onStatusChange) onStatusChange(newStatus);
      toast.success(`Status updated to ${newStatus}`);
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to update status");
    } finally {
      setStatusUpdating(false);
    }
  };

  // Handle rating submission
  const handleRatingSubmit = async () => {
    if (!userId) {
      toast.error("You need to be logged in to rate a project");
      return;
    }

    try {
      setIsSubmittingRating(true);
      const res = await fetch(`${API_BASE}/rate_project`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project_id, user_id: userId, score: ratingValue, comment: ratingComment }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
      setProjectDetails(prev => prev ? { ...prev, rating: ratingValue, has_rated: true } : prev);
      setRatingComment("");
      toast.success(`Rated ${ratingValue}/10 — thanks for your feedback!`);
      setIsRatingDialogOpen(false);
      fetchRatings();
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Failed to submit rating");
    } finally {
      setIsSubmittingRating(false);
    }
  };
  

  const isAdmin = projectDetails?.admin_id !== undefined &&
    String(projectDetails.admin_id) === String(userId);

  const statusLabelMap: Record<string, string> = {
    planning: "Planning",
    running: "Active",
    completed: "Completed",
  };
  const currentStatusLabel = statusLabelMap[projectDetails?.status ?? ""] ?? projectDetails?.project_type ?? "—";

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-black text-white p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center mb-8">
            <Link href="/my-projects" className="text-muted-foreground hover:text-white mr-4">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <h1 className="text-3xl font-bold text-pink-500">Loading Project...</h1>
          </div>
          <div className="bg-zinc-900 rounded-lg border border-zinc-800 p-8 text-center">
            <p className="text-muted-foreground">
              Fetching project details, please wait...
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Project not found or error
  if (!projectDetails) {
    return (
      <div className="min-h-screen bg-black text-white p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center mb-8">
            <Link href="/my-projects" className="text-muted-foreground hover:text-white mr-4">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <h1 className="text-3xl font-bold text-pink-500">Project Not Found</h1>
          </div>
          <div className="bg-zinc-900 rounded-lg border border-zinc-800 p-8 text-center">
            <p className="text-muted-foreground">
              The project you're looking for doesn't exist or you don't have access to it.
            </p>
          </div>
        </div>
      </div>
    );
  }
  
  // Convert tech_stack string to array for rendering
  const techStackArray = projectDetails.tech_stack 
    ? projectDetails.tech_stack.split(',').map(tech => tech.trim())
    : [];
  
  const getStatusStyle = (stepNumber: number) => {
    const currentStatus = projectDetails.status || "running";
    
    if (
      (stepNumber === 1 && currentStatus === "planning") ||
      (stepNumber === 2 && currentStatus === "running") ||
      (stepNumber === 3 && currentStatus === "completed")
    ) {
      return "bg-pink-500";
    }
    
    return "bg-zinc-700";
  };
  
  // Generate stars for rating display
  const renderRatingStars = (rating: number) => {
    const stars = [];
    const filledStars = Math.round(rating); // 0-5 scale
    
    for (let i = 0; i < 5; i++) {
      stars.push(
        <Star 
          key={i}
          className={`h-4 w-4 ${i < filledStars ? "text-yellow-400 fill-yellow-400" : "text-gray-400"}`} 
        />
      );
    }
    
    return stars;
  };
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-6">
          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader className="flex flex-row items-start justify-between gap-4 flex-wrap">
              <div className="flex items-center gap-3">
                <CardTitle>Project Overview</CardTitle>
              </div>

              {/* Rating section — members see current rating, outsiders can rate */}
              <div className="flex flex-col items-end">
                {projectDetails.rating_count && projectDetails.rating_count > 0 ? (
                  <div className="flex items-center gap-1 mb-1">
                    {renderRatingStars(projectDetails.rating ?? 0)}
                    <span className="text-sm text-muted-foreground ml-1">
                      {(projectDetails.rating ?? 0).toFixed(1)}/5
                    </span>
                  </div>
                ) : (
                  <div className="flex items-center gap-1 mb-1">
                    {renderRatingStars(0)}
                    <span className="text-xs text-muted-foreground ml-1">Not rated yet</span>
                  </div>
                )}
                {projectDetails.rating_count !== undefined && projectDetails.rating_count > 0 && (
                  <span className="text-xs text-muted-foreground mb-1">
                    {projectDetails.rating_count} {projectDetails.rating_count === 1 ? "person" : "people"} rated
                  </span>
                )}

                {projectDetails.is_member ? (
                  <span className="text-xs text-muted-foreground">Team member</span>
                ) : projectDetails.status !== "completed" ? (
                  <span className="text-xs text-muted-foreground">Rating opens when project closes</span>
                ) : projectDetails.has_rated ? (
                  <span className="text-xs text-green-500">You rated this project</span>
                ) : (
                  <Dialog open={isRatingDialogOpen} onOpenChange={setIsRatingDialogOpen}>
                    <DialogTrigger asChild>
                      <Button variant="outline" size="sm">
                        Rate Project
                      </Button>
                    </DialogTrigger>
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Rate this project</DialogTitle>
                      </DialogHeader>
                      <div className="py-4">
                        <div className="flex flex-col items-center space-y-6">
                          <div className="flex items-center gap-1">
                            {[...Array(5)].map((_, i) => (
                              <Star
                                key={i}
                                className={`h-8 w-8 ${i < (ratingValue / 2) ? "text-yellow-400 fill-yellow-400" : "text-gray-400"}`}
                              />
                            ))}
                          </div>
                          <div className="w-full px-1">
                            <Slider
                              defaultValue={[ratingValue]}
                              min={1}
                              max={10}
                              step={1}
                              onValueChange={(value) => setRatingValue(value[0])}
                              className="w-full"
                            />
                            <div className="flex justify-between mt-2">
                              <span className="text-sm text-muted-foreground">1</span>
                              <span className="text-sm font-medium">{ratingValue}/10</span>
                              <span className="text-sm text-muted-foreground">10</span>
                            </div>
                          </div>
                          <div className="w-full">
                            <label className="text-sm text-muted-foreground mb-1 block">Comment (optional)</label>
                            <textarea
                              value={ratingComment}
                              onChange={(e) => setRatingComment(e.target.value)}
                              placeholder="Share your thoughts about this project..."
                              rows={3}
                              className="w-full rounded-md border border-zinc-700 bg-zinc-800 px-3 py-2 text-sm text-white placeholder:text-zinc-500 focus:outline-none focus:ring-1 focus:ring-pink-500 resize-none"
                            />
                          </div>
                          <div className="flex justify-end gap-2 w-full mt-4">
                            <DialogClose asChild>
                              <Button variant="outline">Cancel</Button>
                            </DialogClose>
                            <Button
                              onClick={handleRatingSubmit}
                              disabled={isSubmittingRating}
                              className="bg-pink-500 hover:bg-pink-600"
                            >
                              {isSubmittingRating ? "Submitting..." : "Submit Rating"}
                            </Button>
                          </div>
                        </div>
                      </div>
                    </DialogContent>
                  </Dialog>
                )}
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">{projectDetails.description}</p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                <div className="flex items-start">
                  <Briefcase className="h-5 w-5 mr-2 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-sm text-muted-foreground">Project Status</p>
                    <p className="font-medium">{currentStatusLabel}</p>
                  </div>
                </div>

                <div className="flex items-start">
                  <Users className="h-5 w-5 mr-2 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-sm text-muted-foreground">Team Size</p>
                    <p className="font-medium">{projectDetails.project_size}</p>
                  </div>
                </div>

                <div className="flex items-start">
                  <Calendar className="h-5 w-5 mr-2 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-sm text-muted-foreground">Start Date</p>
                    <p className="font-medium">{new Date(projectDetails.start_date).toLocaleDateString()}</p>
                  </div>
                </div>

                <div className="flex items-start">
                  <Clock className="h-5 w-5 mr-2 text-muted-foreground mt-0.5" />
                  <div>
                    <p className="text-sm text-muted-foreground">End Date</p>
                    <p className="font-medium">{new Date(projectDetails.end_date).toLocaleDateString()}</p>
                  </div>
                </div>

                {projectDetails.github_link && (
                  <div className="flex items-start">
                    <Github className="h-5 w-5 mr-2 text-muted-foreground mt-0.5" />
                    <div>
                      <p className="text-sm text-muted-foreground">Github</p>
                      <a 
                        href={projectDetails.github_link}
                        target="_blank"
                        rel="noopener noreferrer" 
                        className="font-medium text-blue-400 hover:underline"
                      >
                        {projectDetails.github_link.replace(/^https?:\/\/(www\.)?/, '')}
                      </a>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle>Tech Stack</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {techStackArray.length > 0 ? (
                  techStackArray.map((tech, index) => (
                    <Badge key={index} className="bg-pink-500/10 text-pink-500 border-pink-500/20">
                      <Code className="h-3 w-3 mr-1" /> {tech}
                    </Badge>
                  ))
                ) : (
                  <p className="text-muted-foreground">No technologies specified for this project.</p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Ratings & Comments */}
          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle>Ratings &amp; Reviews</CardTitle>
            </CardHeader>
            <CardContent>
              {projectRatings.length === 0 ? (
                <p className="text-muted-foreground text-sm">No reviews yet.</p>
              ) : (
                <div className="space-y-4">
                  {projectRatings.map((r, i) => (
                    <div key={i} className="border-b border-zinc-800 pb-4 last:border-0 last:pb-0">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-white">{r.reviewer_name}</span>
                        <div className="flex items-center gap-1">
                          {[...Array(5)].map((_, s) => (
                            <Star
                              key={s}
                              className={`h-3.5 w-3.5 ${s < Math.round(r.score) ? "text-yellow-400 fill-yellow-400" : "text-zinc-600"}`}
                            />
                          ))}
                          <span className="text-xs text-muted-foreground ml-1">{r.score}/5</span>
                        </div>
                      </div>
                      {r.comment && (
                        <p className="text-sm text-zinc-400 leading-relaxed">{r.comment}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          {/* Project Status Card */}
          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader className="pb-3">
              <div className="flex justify-between items-center">
                <CardTitle className="text-sm font-medium">Project Status</CardTitle>
                {isAdmin && (
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="outline"
                        size="sm"
                        disabled={statusUpdating}
                        className="text-xs"
                      >
                        {statusUpdating ? "Updating…" : "Change"}
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleStatusChange("planning")}>
                        Planning
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleStatusChange("running")}>
                        Running
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleStatusChange("completed")}>
                        Completed
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                )}
              </div>
            </CardHeader>
            <CardContent>
              {/* Status Progress Indicator */}
              <div className="flex items-center justify-between">
                {/* Progress Bar Line */}
              
                {/* Status Circles */}
                <div className="relative flex justify-between w-full z-10">
                  {/* Planning Circle */}
                  <div className="flex flex-col items-center">
                    <div className={`w-5 h-5 rounded-full ${getStatusStyle(1)}`}></div>
                    <span className="text-xs mt-1">Planning</span>
                  </div>
                  
                  {/* Running Circle */}
                  <div className="flex flex-col items-center">
                    <div className={`w-5 h-5 rounded-full ${getStatusStyle(2)}`}></div>
                    <span className="text-xs mt-1">Running</span>
                  </div>
                  
                  {/* Completed Circle */}
                  <div className="flex flex-col items-center">
                    <div className={`w-5 h-5 rounded-full ${getStatusStyle(3)}`}></div>
                    <span className="text-xs mt-1">Completed</span>
                  </div>
                </div>
              </div>
              
              <div className="mt-3 text-center">
                <p className="text-sm font-medium">
                  <span className="capitalize">{projectDetails.status || "Running"}</span>
                </p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900 border-zinc-800">
            <CardHeader>
              <CardTitle>Team Members</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {projectDetails.team_members && projectDetails.team_members.length > 0 ? (
                  projectDetails.team_members.map((member, index) => (
                    <div key={index} className="flex items-center">
                      <Avatar className="h-8 w-8 mr-2">
                        <AvatarImage src={`/placeholder.svg?height=32&width=32`} />
                        <AvatarFallback>
                          {member.split(' ').map(word => word[0]).join('').toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <span>{member}</span>
                    </div>
                  ))
                ) : (
                  <p className="text-muted-foreground">No team members have been added to this project.</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
