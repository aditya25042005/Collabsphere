"use client";
import { useState, useEffect } from "react";
import { API_BASE } from "@/lib/api";
import { useParams } from "next/navigation"; // Add useParams
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Plus, X, Github, Linkedin } from "lucide-react";
import { useRouter } from "next/navigation";
// MUI icons
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutlined";
import LogoutIcon from "@mui/icons-material/Logout";
import EmojiEventsIcon from "@mui/icons-material/EmojiEvents";
import EmailIcon from "@mui/icons-material/Email";
import PersonIcon from "@mui/icons-material/Person";
import GroupsIcon from "@mui/icons-material/Groups";
import WorkspacesIcon from "@mui/icons-material/Workspaces";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutlined";
import StarIcon from "@mui/icons-material/Star";
import Navbar from "@/components/navbar";
import { useUserContext } from "@/lib/usercontext";

export default function SettingsPage() {
  const router = useRouter();
  const params = useParams(); /// Get URL parameters
  const profileUserId = params?.id as string; // Get the profile ID from URL

  const [activeNav, setActiveNav] = useState("profile");
  const [tech, setTech] = useState("");
  const [techStack, setTechStack] = useState<string[]>([]);
  const [isOwnProfile, setIsOwnProfile] = useState(false); // Add state to track if viewing own profile
  const [activeTab, setActiveTab] = useState("profile"); // Track active tab
  const [projectFilter, setProjectFilter] = useState<"all" | "active" | "completed">("all");
  // Moved inside the component
  const [userData, setuserData] = useState<User>({
    name: "",
    email: "",
    email_update: false, // Default value for email_update
    github_profile: "",
    linkedin_profile: "",
    past_experience: "",
    project_update: false, // Default value for project_update
    roll_no: 0, // Default value for roll_no
    rating: 0, // Default value for rating (e.g., 0 for no rating)
    role_type: "", // Default value for role_type (empty string for initial state)
    tech_stack: [], // Initialize tech_stack as an empty array
  });
const {user } = useUserContext()
const userlocal = typeof window !== 'undefined' ? localStorage.getItem('user') : null;
const parsedUser = userlocal ? JSON.parse(userlocal) : null;
  const userId = user?.id ? user?.id : parsedUser?.id;
  const handleAddTech = () => {
    if (tech.trim() !== "") {
      setTechStack((prev) => [...prev, tech.trim()]);
      setuserData((prev) => ({
        ...prev, // Spread the previous state
        tech_stack: [...prev.tech_stack, tech], // Add the new value to the tech_stack array
      }));
      setTech("");

    }
  };

   useEffect(() => {
    if (userId && profileUserId) {
      const isOwner = userId === profileUserId;
      setIsOwnProfile(isOwner);
      console.log("Is own profile:", isOwner, "userId:", userId, "profileUserId:", profileUserId);
      
      // Reset to profile tab if settings was selected but it's not the user's profile
      if (!isOwner && activeTab === "settings") {
        setActiveTab("profile");
      }
    }
  }, [userId, profileUserId, activeTab]);
  
  const handleRemoveTech = (itemToRemove: string) => {
    setTechStack((prev) => prev.filter((item) => item !== itemToRemove));
  };
  const [roll_no, setroll_no] = useState(3);
  interface User {
    name:string;
    email: string; // Email address of the user
    email_update: boolean; // Whether email updates are enabled
    github_profile: string; // GitHub profile URL
    linkedin_profile: string; // LinkedIn profile URL
    past_experience: string; // Description of past experience
    project_update: boolean; // Whether project updates are enabled
    rating: number; // User rating (e.g., 4.8)
    role_type: string; // Role type (e.g., "professor")
    roll_no: number; // Roll number or unique identifier
    tech_stack: string[]; // Array of technical skills
  }
  const [profile, setProfile] = useState<User[]>([]);
  useEffect(() => {
    if (!profileUserId) return;
    const fetchData = async () => {
      try {
        const response = await fetch(`${API_BASE}/profile/view`, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ roll_no: profileUserId }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("API Response: line 176", data);
        setProfile(data.user ?? []);
        if (data.user?.[0]) setuserData(data.user[0]);
        console.log("Server Response:", data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, [profileUserId]);
  const [project_setting, setProjectSetting] = useState<Project[]>([]);
  useEffect(() => {
    if (!profileUserId) return;
    const fetchCurrentProjects = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/list/current/projects`,
          {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: profileUserId }),
          }
        );

        if (!response.ok) {
          console.log("Error:", response.status);
          return;
        }

        const data = await response.json();
        setProjectSetting(data.project ?? []);
      } catch (error) {
        console.error("Error fetching current projects:", error);
      }
    };
    fetchCurrentProjects();
  }, [profileUserId]);

  interface Project {
    admin_id: number;
    role: string;
    end_date: string;
    members_required: number;
    current_members?: number;
    project_id: number;
    start_date: string;
    status: string;
    tags: string;
    title: string;
  }
  const [past_projects, setPastprojects] = useState<Past[]>([]);
  useEffect(() => {
    if (!profileUserId) return;
    const fetchPastProjects = async () => {
      try {
        const response = await fetch(
          `${API_BASE}/list/past/projects`,
          {
            method: "POST",
            credentials: "include",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: profileUserId }),
          }
        );

        if (!response.ok) {
          console.log("Error:", response.status);
          return;
        }

        const data = await response.json();
        setPastprojects(data.project ?? []);
      } catch (error) {
        console.error("Error fetching past projects:", error);
      }
    };
    fetchPastProjects();
  }, [profileUserId]);
  interface Past {
    admin_id: number;
    role: string;
    end_date: string;
    members_required: number;
    current_members?: number;
    project_id: number;
    start_date: string;
    status: string;
    tags: string;
    title: string;
  }

  interface RatingGiven {
    score: number;
    comment: string;
    created_at: string | null;
    project_title: string;
    project_id: number;
  }
  interface MemberRatingReceived {
    score: number;
    comment: string;
    created_at: string | null;
    project_title: string;
    project_id: number;
    rated_by_name: string;
  }

  const [ratingsGiven, setRatingsGiven] = useState<RatingGiven[]>([]);
  const [memberRatings, setMemberRatings] = useState<MemberRatingReceived[]>([]);

  useEffect(() => {
    if (!profileUserId) return;
    fetch(`${API_BASE}/user/ratings/given?user_id=${profileUserId}`, { credentials: "include" })
      .then(r => r.json())
      .then(d => setRatingsGiven(d.ratings ?? []))
      .catch(() => {});
    fetch(`${API_BASE}/user/ratings/received?user_id=${profileUserId}`, { credentials: "include" })
      .then(r => r.json())
      .then(d => setMemberRatings(d.ratings ?? []))
      .catch(() => {});
  }, [profileUserId]);

  const renderStars = (score: number, outOf = 5) => {
    const filled = Math.round(score);
    return (
      <span className="flex gap-0.5">
        {Array.from({ length: outOf }).map((_, i) => (
          <span key={i} className={i < filled ? "text-yellow-400" : "text-zinc-600"}>★</span>
        ))}
      </span>
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Prepare the data to match the API's expected format
    const profileData = {
      past_experience: userData.past_experience,
      tech_stack : [...userData.tech_stack],

      github_profile: userData.github_profile,
      linkedin_profile: userData.linkedin_profile,
      email_update: userData.email_update,
      project_update: userData.project_update,
      roll_no: userId,
    };
    try {
      console.log(profileData);
      // Make the API call using your existing API endpoint
      const response = await fetch(`${API_BASE}/update/profile`, {
        method: "POST",
        credentials: "include", // Include cookies if needed
        headers: {
          "Content-Type": "application/json", // Specify JSON data
        },
        body: JSON.stringify(profileData), // Send the prepared data
      });
      // Check for errors in the response
      if (!response.ok) {
       console.log("Error:", response.status);
      }
      // Parse the response data
      const data = await response.json();
      console.log("Server Response:", data);
      // Redirect to the profile page
      alert("Changes Saved")
    } catch (error) {
      console.error("Error submitting profile data:", error);
    }
  };
  
  const initials = userData.name
    ? userData.name.split(" ").map((n: string) => n[0]).join("").toUpperCase().slice(0, 2)
    : profileUserId?.slice(0, 2).toUpperCase() ?? "??";

  const skillColors = [
    "bg-pink-500/15 text-pink-300 border-pink-500/30",
    "bg-fuchsia-500/15 text-fuchsia-300 border-fuchsia-500/30",
    "bg-purple-500/15 text-purple-300 border-purple-500/30",
    "bg-violet-500/15 text-violet-300 border-violet-500/30",
    "bg-rose-500/15 text-rose-300 border-rose-500/30",
  ];

  return (
    <div className="flex min-h-screen bg-[#09090b] text-white">
      <Navbar activeNav={activeNav} setActiveNav={setActiveNav} />

      <div className="flex-1 overflow-y-auto min-w-0">

        {/* ── Hero banner — avatar anchored to bottom edge ── */}
        <div className="relative h-28 sm:h-36 border-b border-zinc-800" style={{ background: "linear-gradient(135deg, #831843 0%, #701a75 40%, #4a044e 70%, #18181b 100%)" }}>
          <div className="absolute inset-0 opacity-30"
            style={{ backgroundImage: "radial-gradient(circle, #f472b6 1px, transparent 1px)", backgroundSize: "20px 20px" }} />
          <div className="absolute inset-0" style={{ background: "radial-gradient(ellipse at 30% 50%, rgba(236,72,153,0.25) 0%, transparent 60%)" }} />
          {/* Avatar: half inside banner, half below */}
          <div className="absolute bottom-0 left-4 sm:left-8 translate-y-1/2 z-10">
            <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-zinc-900 ring-4 ring-[#09090b] flex items-center justify-center text-lg sm:text-xl font-black text-pink-400 shadow-xl">
              {initials}
            </div>
          </div>
        </div>

        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-16">

          {/* ── Name row — always on dark bg, clear of banner ── */}
          <div className="pt-10 sm:pt-12 mb-6 sm:mb-8 flex items-start justify-between gap-3">
            <div className="pl-20 sm:pl-24 min-w-0">
              <h1 className="text-lg sm:text-2xl font-bold text-white truncate">{userData.name || profileUserId}</h1>
              <p className="text-zinc-400 text-xs sm:text-sm truncate">{userData.role_type || "Member"} · {profileUserId}</p>
            </div>

            {isOwnProfile && (
              <div className="flex items-center gap-2 flex-shrink-0">
                <Button
                  size="sm"
                  variant="outline"
                  className="border-zinc-700 text-zinc-400 hover:text-white hover:border-pink-500"
                  onClick={() => setActiveTab("settings")}
                >
                  Edit Profile
                </Button>
                <Link href="/create_project">
                  <Button size="sm" className="bg-pink-600 hover:bg-pink-700 text-white">
                    <AddCircleOutlineIcon style={{ fontSize: 14, marginRight: 4 }} /> New Project
                  </Button>
                </Link>
                <Button
                  size="sm"
                  variant="outline"
                  className="border-zinc-700 text-zinc-400 hover:text-white hover:border-zinc-500"
                  onClick={async () => {
                    await fetch(`${API_BASE}/logout`, { method: "GET", credentials: "include" });
                    localStorage.removeItem("user");
                    localStorage.removeItem("token");
                    window.location.href = "/";
                  }}
                >
                  <LogoutIcon style={{ fontSize: 14, marginRight: 4 }} /> Logout
                </Button>
              </div>
            )}
          </div>

          {/* ── Stat chips ───────────────────────────────── */}
          <div className="flex flex-wrap gap-2 sm:gap-3 mb-6 sm:mb-8">
            {[
              { label: "Rating",    value: userData.rating?.toFixed?.(1) ?? "—", Icon: StarIcon,                color: "#facc15" },
              { label: "Active",    value: project_setting?.length ?? 0,          Icon: WorkspacesIcon,          color: "#f472b6" },
              { label: "Completed", value: past_projects?.length ?? 0,            Icon: CheckCircleOutlineIcon,  color: "#34d399" },
            ].map(({ label, value, Icon, color }) => (
              <div key={label} className="flex items-center gap-2.5 bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-2.5">
                <Icon style={{ fontSize: 20, color }} />
                <div>
                  <p className="text-base font-bold text-white leading-none">{value}</p>
                  <p className="text-[11px] text-zinc-500 mt-0.5">{label}</p>
                </div>
              </div>
            ))}
          </div>

          {/* ── Tabs ─────────────────────────────────────── */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="bg-zinc-900 border border-zinc-800 rounded-xl p-1 mb-6 w-fit">
              <TabsTrigger value="profile" className="rounded-lg data-[state=active]:bg-pink-600 data-[state=active]:text-white text-zinc-400 px-5">
                Profile
              </TabsTrigger>
              <TabsTrigger value="projects" className="rounded-lg data-[state=active]:bg-pink-600 data-[state=active]:text-white text-zinc-400 px-5">
                Projects
              </TabsTrigger>
              {isOwnProfile && (
                <TabsTrigger value="settings" className="rounded-lg data-[state=active]:bg-pink-600 data-[state=active]:text-white text-zinc-400 px-5">
                  Settings
                </TabsTrigger>
              )}
            </TabsList>

          {/* ── Profile tab ─────────────────────────────── */}
          <TabsContent value="profile" className="space-y-5">
            {(profile ?? []).map((u, index) => (
              <div key={index} className="grid md:grid-cols-[240px_1fr] gap-5">

                {/* Left sidebar */}
                <div className="space-y-4">
                  {/* Contact card */}
                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5 space-y-3">
                    <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500">Contact</p>
                    {u.email && (
                      <div className="flex items-center gap-2.5 text-sm text-zinc-300">
                        <EmailIcon style={{ fontSize: 16, color: "#f472b6", flexShrink: 0 }} />
                        <span className="truncate">{u.email}</span>
                      </div>
                    )}
                    {u.github_profile && (
                      <a href={u.github_profile} target="_blank" rel="noopener noreferrer"
                        className="flex items-center gap-2.5 text-sm text-zinc-300 hover:text-pink-300 transition-colors">
                        <Github className="h-4 w-4 text-pink-400 flex-shrink-0" />
                        <span className="truncate">GitHub</span>
                      </a>
                    )}
                    {u.linkedin_profile && (
                      <a href={u.linkedin_profile} target="_blank" rel="noopener noreferrer"
                        className="flex items-center gap-2.5 text-sm text-zinc-300 hover:text-pink-300 transition-colors">
                        <Linkedin className="h-4 w-4 text-pink-400 flex-shrink-0" />
                        <span className="truncate">LinkedIn</span>
                      </a>
                    )}
                  </div>
                </div>

                {/* Right main */}
                <div className="space-y-5">
                  {/* Bio */}
                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500 mb-3">About</p>
                    <p className="text-zinc-300 text-sm leading-relaxed">
                      {u.past_experience || "No bio yet."}
                    </p>
                  </div>

                  {/* Skills */}
                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500 mb-3">Tech Stack</p>
                    {(u.tech_stack ?? []).length === 0 ? (
                      <p className="text-zinc-500 text-sm">No skills added yet.</p>
                    ) : (
                      <div className="flex flex-wrap gap-2">
                        {(u.tech_stack ?? []).map((skill, i) => (
                          <span key={i}
                            className={`px-3 py-1 rounded-full text-xs font-medium border ${skillColors[i % skillColors.length]}`}>
                            {skill}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Member ratings received */}
                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <div className="flex items-center justify-between mb-4">
                      <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500">Team Ratings</p>
                      {u.rating > 0 && (
                        <span className="flex items-center gap-1 text-yellow-400 text-sm font-semibold">
                          <StarIcon style={{ fontSize: 15 }} />
                          {Number(u.rating).toFixed(1)}
                        </span>
                      )}
                    </div>
                    {memberRatings.length === 0 ? (
                      <p className="text-zinc-500 text-sm">No team ratings yet.</p>
                    ) : (
                      <div className="space-y-3">
                        {memberRatings.map((r, i) => (
                          <div key={i} className="border border-zinc-800 rounded-xl p-3 space-y-1">
                            <div className="flex items-center justify-between gap-2">
                              <Link href={`/project/${r.project_id}`} className="text-xs text-pink-400 hover:underline truncate">{r.project_title}</Link>
                              {renderStars(r.score)}
                            </div>
                            {r.comment && <p className="text-zinc-400 text-xs leading-relaxed">{r.comment}</p>}
                            <p className="text-zinc-600 text-[11px]">by {r.rated_by_name}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Project ratings given */}
                  <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-5">
                    <p className="text-xs font-semibold uppercase tracking-widest text-zinc-500 mb-4">Project Reviews Given</p>
                    {ratingsGiven.length === 0 ? (
                      <p className="text-zinc-500 text-sm">No project reviews yet.</p>
                    ) : (
                      <div className="space-y-3">
                        {ratingsGiven.map((r, i) => (
                          <div key={i} className="border border-zinc-800 rounded-xl p-3 space-y-1">
                            <div className="flex items-center justify-between gap-2">
                              <Link href={`/project/${r.project_id}`} className="text-xs text-pink-400 hover:underline truncate">{r.project_title}</Link>
                              <span className="flex items-center gap-1 text-yellow-400 text-xs font-semibold">
                                <StarIcon style={{ fontSize: 13 }} />
                                {Number(r.score).toFixed(1)}/5
                              </span>
                            </div>
                            {r.comment && <p className="text-zinc-400 text-xs leading-relaxed">{r.comment}</p>}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </TabsContent>

          {/* ── Projects tab ────────────────────────────── */}
          <TabsContent value="projects" className="space-y-6">

            {/* Filter chips */}
            <div className="flex items-center gap-2 flex-wrap">
              {(["all", "active", "completed"] as const).map((f) => {
                const labels = { all: "All", active: "Active", completed: "Completed" };
                const styles = {
                  all: projectFilter === "all"
                    ? "bg-pink-500 text-white border-pink-500"
                    : "bg-transparent text-zinc-400 border-zinc-700 hover:border-zinc-500",
                  active: projectFilter === "active"
                    ? "bg-emerald-500/20 text-emerald-400 border-emerald-500"
                    : "bg-transparent text-zinc-400 border-zinc-700 hover:border-zinc-500",
                  completed: projectFilter === "completed"
                    ? "bg-zinc-700 text-zinc-200 border-zinc-500"
                    : "bg-transparent text-zinc-400 border-zinc-700 hover:border-zinc-500",
                };
                const counts = {
                  all: (project_setting ?? []).length + (past_projects ?? []).length,
                  active: (project_setting ?? []).length,
                  completed: (past_projects ?? []).length,
                };
                return (
                  <button
                    key={f}
                    onClick={() => setProjectFilter(f)}
                    className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold border transition-all ${styles[f]}`}
                  >
                    {f === "active" && <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />}
                    {f === "completed" && <span className="w-1.5 h-1.5 rounded-full bg-zinc-400" />}
                    {labels[f]}
                    <span className="opacity-60 font-normal">{counts[f]}</span>
                  </button>
                );
              })}
            </div>

            {/* Active projects */}
            {(projectFilter === "all" || projectFilter === "active") && (
              <div>
                {projectFilter === "all" && (
                  <div className="flex items-center gap-2 mb-4">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                    <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400">Active Projects</h3>
                  </div>
                )}
                {(project_setting ?? []).length === 0 ? (
                  <p className="text-zinc-500 text-sm">No active projects.</p>
                ) : (
                  <div className="grid sm:grid-cols-2 gap-4">
                    {(project_setting ?? []).map((project) => (
                      <Link key={project.project_id} href={`/project/${project.project_id}`}>
                        <div className="bg-zinc-900 border border-zinc-800 hover:border-pink-500/50 rounded-2xl p-5 flex flex-col gap-3 transition-colors cursor-pointer h-full">
                          <div className="flex items-start justify-between gap-2">
                            <h4 className="font-semibold text-white text-sm leading-snug">{project.title}</h4>
                            <span className="flex-shrink-0 text-[10px] font-semibold uppercase tracking-wide bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 rounded-full px-2.5 py-0.5">
                              Active
                            </span>
                          </div>
                          <div className="flex items-center gap-3 text-xs text-zinc-500">
                            <span className="flex items-center gap-1"><PersonIcon style={{ fontSize: 13 }} /> {project.role || "Member"}</span>
                            <span className="flex items-center gap-1">
                              <GroupsIcon style={{ fontSize: 13 }} />
                              {project.current_members !== undefined
                                ? `${project.current_members}/${project.members_required}`
                                : project.members_required} members
                            </span>
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Past projects */}
            {(projectFilter === "all" || projectFilter === "completed") && (
              <div>
                {projectFilter === "all" && (
                  <div className="flex items-center gap-2 mb-4">
                    <span className="w-2 h-2 rounded-full bg-zinc-500" />
                    <h3 className="text-sm font-semibold uppercase tracking-widest text-zinc-400">Past Projects</h3>
                  </div>
                )}
                {(past_projects ?? []).length === 0 ? (
                  <p className="text-zinc-500 text-sm">No completed projects yet.</p>
                ) : (
                  <div className="grid sm:grid-cols-2 gap-4">
                    {(past_projects ?? []).map((project) => (
                      <Link key={project.project_id} href={`/project/${project.project_id}`}>
                        <div className="bg-zinc-900 border border-zinc-800 hover:border-zinc-600 rounded-2xl p-5 flex flex-col gap-3 opacity-80 hover:opacity-100 transition-all cursor-pointer h-full">
                          <div className="flex items-start justify-between gap-2">
                            <h4 className="font-semibold text-white text-sm leading-snug">{project.title}</h4>
                            <span className="flex-shrink-0 text-[10px] font-semibold uppercase tracking-wide bg-zinc-700 text-zinc-400 border border-zinc-600 rounded-full px-2.5 py-0.5">
                              Done
                            </span>
                          </div>
                          <div className="flex items-center gap-3 text-xs text-zinc-500">
                            <span className="flex items-center gap-1"><PersonIcon style={{ fontSize: 13 }} /> {project.role || "Member"}</span>
                            <span className="flex items-center gap-1">
                              <GroupsIcon style={{ fontSize: 13 }} />
                              {project.current_members !== undefined
                                ? `${project.current_members}/${project.members_required}`
                                : project.members_required} members
                            </span>
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Empty state when filtered */}
            {projectFilter === "active" && (project_setting ?? []).length === 0 && (
              <p className="text-zinc-500 text-sm">No active projects.</p>
            )}
            {projectFilter === "completed" && (past_projects ?? []).length === 0 && (
              <p className="text-zinc-500 text-sm">No completed projects yet.</p>
            )}

          </TabsContent>
          {isOwnProfile && (<TabsContent value="settings" className="space-y-6">
            <Card className="bg-gray-800 border-none">
              <CardHeader>
                <CardTitle className="text-pink-500">
                  Account Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Full Name */}
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    value={userData.name || ''} // Use empty string as fallback
                    readOnly
                    onChange={(e) =>
                      setuserData((prev) => ({ ...prev, name: e.target.value }))
                    }
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                {/* Email */}
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    value={userData.email || ''} // Use empty string as fallback
                    readOnly
                    onChange={(e) =>
                      setuserData((prev) => ({
                        ...prev,
                        email: e.target.value,
                      }))
                    }
                    className="bg-gray-700 border-gray-600 cursor-not-allowed"
                  />
                </div>
                {/* LinkedIn */}
                <div className="space-y-2">
                  <Label htmlFor="linkedIn">LinkedIn</Label>
                  <Input
                    id="linkedin"
                    value={userData.linkedin_profile || ''} // Use empty string as fallback
                    onChange={(e) =>
                      setuserData((prev) => ({
                        ...prev,
                        linkedin_profile: e.target.value, // Fixed property name
                      }))
                    }
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                {/* GitHub */}
                <div className="space-y-2">
                  <Label htmlFor="github">GitHub</Label>
                  <Input
                    id="github"
                    value={userData.github_profile || ''} // Use empty string as fallback
                    onChange={(e) =>
                      setuserData((prev) => ({
                        ...prev,
                        github_profile: e.target.value,
                      }))
                    }
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                {/* Past Experience */}
                <div className="space-y-2">
                  <Label htmlFor="pastexperience">Past Experience</Label>
                  <Input
                    id="pastexperience"
                    value={userData.past_experience || ''} // Use empty string as fallback
                    onChange={(e) =>
                      setuserData((prev) => ({
                        ...prev,
                        past_experience: e.target.value,
                      }))
                    }
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                {/* Tech Stack (New Section) */}
                <div>
                  <label className="block text-sm mb-1">Tech Stack</label>
                  <div className="flex gap-2">
                    <Input
                      placeholder="Add technology"
                      className="bg-zinc-800 border-zinc-700"
                      onChange={(e) =>
                      {setTech(e.target.value)}
                      }
                      
                    
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="icon"
                      onClick={handleAddTech}
                      className="border-zinc-700"
                    >
                      <Plus className="h-4 w-4" />
                    </Button>
                  </div>
                  {userData.tech_stack.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-2">
                      {(userData.tech_stack ?? []).map((item, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="bg-zinc-800 text-white"
                        >
                          {item}
                          <button
                            type="button"
                            onClick={() => handleRemoveTech(item)}
                            className="ml-1 text-zinc-400 hover:text-white"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
                {/* Save Changes Button */}
                <Button
                  className="bg-pink-500 hover:bg-pink-600 w-full"
                  onClick={(e) => {
                    handleSubmit(e);
                  }}
                >
                  Save Changes
                </Button>
              </CardContent>
            </Card>
          </TabsContent>)}
          
          {/* Settings Tab */}
          {/* <TabsContent value="settings" className="space-y-6">
            <Card className="bg-gray-800 border-none">
              <CardHeader>
                <CardTitle className="text-pink-500">
                  Account Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  <Input
                    id="name"
                    defaultValue={userData.name}
                    className="bg-gray-700 border-gray-600"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    defaultValue={userData.email}
                    className="bg-gray-700 border-gray-600"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="linkedIn">LinkedIn</Label>
                  <Input
                    id="linkedin"
                    defaultValue={userData.linkedin}
                    className="bg-gray-700 border-gray-600"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="github">GithHub</Label>
                  <Input
                    id="github"
                    defaultValue={userData.github}
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="pastexperience">Past Experience</Label>
                  <Input
                    id="pastexperience"
                    defaultValue={userData.bio}
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="techstack">Tech Stack</Label>
                  <Input
                    id="techstack"
                    defaultValue={userData.skills}
                    className="bg-gray-700 border-gray-600"
                  />
                </div>

                <Button className="bg-pink-500 hover:bg-pink-600 w-full">
                  Save Changes
                </Button>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-none">
              
              <CardContent className="space-y-6">
                <div className="pt-4 border-t border-gray-700">
                  <Button variant="destructive" className="w-full">
                    <LogoutIcon style={{ fontSize: 16, marginRight: 6 }} /> Logout
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent> */}
          </Tabs>
        </div>
      </div>
    </div>
  );
}