"use client";
import { useState, useEffect, useRef, useCallback } from "react";
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import TeamMemberCard from "@/components/team-member-card";
import { Search, X } from "lucide-react";
import Navbar from "@/components/navbar";
import { API_BASE } from "@/lib/api";

interface UserProfile {
  email: string;
  email_update: boolean;
  github_profile: string;
  linkedin_profile: string;
  name: string;
  past_experience: string;
  project_count: number;
  project_update: boolean;
  rating: number;
  role_type: string;
  roll_no: number;
  tech_stack: string[];
}

const PAGE_SIZE = 10;

function processUser(user: Partial<UserProfile>): UserProfile {
  return {
    email: user.email || "",
    email_update: user.email_update || false,
    github_profile: user.github_profile || "",
    linkedin_profile: user.linkedin_profile || "",
    name: user.name || "Unknown",
    past_experience: user.past_experience || "",
    project_count: user.project_count || 0,
    project_update: user.project_update || false,
    rating: user.rating || 0,
    role_type: user.role_type || "",
    roll_no: user.roll_no || 0,
    tech_stack: Array.isArray(user.tech_stack)
      ? user.tech_stack
      : typeof user.tech_stack === "string"
      ? [user.tech_stack]
      : [],
  };
}

export default function TeamPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const [dropdownUsers, setDropdownUsers] = useState<UserProfile[]>([]);
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [userProfile, setUserProfile] = useState<UserProfile[]>([]);
  const [allSkills, setAllSkills] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);
  const [dropdownLoading, setDropdownLoading] = useState(false);
  const sentinelRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const buildUrl = (lim: number, off: number, search = "", skills: string[] = []) => {
    const params = new URLSearchParams({ limit: String(lim), offset: String(off) });
    if (search) params.set("search", search);
    skills.forEach(s => params.append("skill", s));
    return `${API_BASE}/list/users?${params}`;
  };

  const fetchPage = useCallback(async (currentOffset: number, replace: boolean, search = "", skills: string[] = []) => {
    replace ? setLoading(true) : setLoadingMore(true);
    try {
      const res = await fetch(buildUrl(PAGE_SIZE, currentOffset, search, skills), { credentials: "include" });
      if (!res.ok) throw new Error();
      const raw = await res.json();
      const incoming: UserProfile[] = (raw.projects ?? []).map(processUser);
      setUserProfile(prev => replace ? incoming : [...prev, ...incoming]);
      setHasMore(currentOffset + incoming.length < (raw.total ?? 0));
      setOffset(currentOffset + incoming.length);
    } catch {
      /* silently fail */
    } finally {
      replace ? setLoading(false) : setLoadingMore(false);
    }
  }, []);

  // Fetch skills list from API once
  useEffect(() => {
    fetch(`${API_BASE}/list/skills`, { credentials: "include" })
      .then(r => r.json())
      .then(d => setAllSkills(d.skills ?? []))
      .catch(() => {});
  }, []);

  // Reload when search or skills filter changes
  useEffect(() => {
    setOffset(0);
    setHasMore(true);
    fetchPage(0, true, searchQuery, selectedSkills);
  }, [searchQuery, selectedSkills]);

  // Infinite scroll
  useEffect(() => {
    if (!sentinelRef.current) return;
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loadingMore && !loading) {
          fetchPage(offset, false, searchQuery, selectedSkills);
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [hasMore, loadingMore, loading, offset, fetchPage, searchQuery, selectedSkills]);

  // Search dropdown — debounced 450ms (fires only after user stops typing)
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!searchInput.trim()) {
      setDropdownUsers([]);
      setShowDropdown(false);
      setDropdownLoading(false);
      return;
    }
    setDropdownLoading(true);
    setShowDropdown(true);
    debounceRef.current = setTimeout(async () => {
      try {
        const res = await fetch(buildUrl(6, 0, searchInput.trim()), { credentials: "include" });
        if (!res.ok) return;
        const raw = await res.json();
        setDropdownUsers((raw.projects ?? []).map(processUser));
      } catch { /* ignore */ } finally {
        setDropdownLoading(false);
      }
    }, 150);
    return () => { if (debounceRef.current) clearTimeout(debounceRef.current); };
  }, [searchInput]);

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(e.target as Node)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const handleDropdownSelect = (user: UserProfile) => {
    setShowDropdown(false);
    setSearchInput("");
  };

  const applySearch = () => {
    setSearchQuery(searchInput.trim());
    setShowDropdown(false);
  };

  const clearSearch = () => {
    setSearchInput("");
    setSearchQuery("");
    setShowDropdown(false);
  };

  const toggleSkill = (skill: string) => {
    setSelectedSkills(prev =>
      prev.includes(skill) ? prev.filter(s => s !== skill) : [...prev, skill]
    );
  };

  const filteredMembers = userProfile.filter(member => {
    if (!member || typeof member.name !== "string") return false;
    return (
      selectedSkills.length === 0 ||
      selectedSkills.every(skill => member.tech_stack.includes(skill))
    );
  });

  return (
    <div className="flex min-h-screen bg-[#09090b]">
      <Navbar activeNav="users" setActiveNav={() => {}} />
      <main className="flex-1 min-w-0 text-white p-4 md:p-8 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-pink-500 mb-8">Team Members</h1>
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-8">

            {/* Sidebar */}
            <div className="lg:col-span-1 space-y-6">

              {/* Search */}
              <div className="bg-zinc-900 rounded-lg border border-zinc-800 p-4">
                <h2 className="text-lg font-semibold mb-4">Search</h2>
                <div className="relative" ref={searchRef}>
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-zinc-400 z-10" />
                  <Input
                    placeholder="Search by name or email..."
                    className="pl-9 pr-8 bg-zinc-800 border-zinc-700"
                    value={searchInput}
                    onChange={e => setSearchInput(e.target.value)}
                    onKeyDown={e => { if (e.key === "Enter") applySearch(); if (e.key === "Escape") setShowDropdown(false); }}
                    onFocus={() => { if (dropdownUsers.length > 0) setShowDropdown(true); }}
                  />
                  {searchInput && (
                    <button onClick={clearSearch} className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-white">
                      <X className="h-3.5 w-3.5" />
                    </button>
                  )}

                  {/* Dropdown */}
                  {showDropdown && (
                    <div className="absolute z-50 top-full mt-1 left-0 right-0 bg-zinc-900 border border-zinc-700 rounded-lg shadow-xl overflow-hidden">
                      {dropdownLoading ? (
                        <div className="flex items-center gap-2 px-3 py-3 text-zinc-500 text-xs">
                          <div className="flex gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: "0ms" }} />
                            <span className="w-1.5 h-1.5 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: "150ms" }} />
                            <span className="w-1.5 h-1.5 rounded-full bg-zinc-500 animate-bounce" style={{ animationDelay: "300ms" }} />
                          </div>
                          Searching...
                        </div>
                      ) : dropdownUsers.length > 0 ? (
                        <>
                          {dropdownUsers.map(user => (
                            <Link
                              key={user.roll_no}
                              href={`/profile/${user.roll_no}`}
                              onClick={() => handleDropdownSelect(user)}
                              className="flex flex-col px-3 py-2.5 hover:bg-zinc-800 transition-colors border-b border-zinc-800 last:border-0"
                            >
                              <span className="text-sm font-medium text-white truncate">{user.name}</span>
                              <span className="text-xs text-zinc-400 truncate">{user.email}</span>
                            </Link>
                          ))}
                          <button
                            onClick={applySearch}
                            className="w-full px-3 py-2 text-xs text-pink-400 hover:bg-zinc-800 text-left border-t border-zinc-800"
                          >
                            See all results for "{searchInput}"
                          </button>
                        </>
                      ) : (
                        <div className="px-3 py-3 text-zinc-500 text-xs">No users found</div>
                      )}
                    </div>
                  )}
                </div>
                {searchQuery && (
                  <div className="flex items-center gap-2 mt-3">
                    <span className="text-xs text-zinc-400">Showing results for:</span>
                    <span className="flex items-center gap-1 bg-pink-500/10 text-pink-400 border border-pink-500/20 rounded-full px-2 py-0.5 text-xs">
                      {searchQuery}
                      <button onClick={clearSearch}><X className="h-3 w-3" /></button>
                    </span>
                  </div>
                )}
              </div>

              {/* Skills Filter */}
              <div className="bg-zinc-900 rounded-lg border border-zinc-800 p-4">
                <h2 className="text-lg font-semibold mb-4">Filter by Skills</h2>
                <div className="flex flex-wrap gap-2">
                  {allSkills.map(skill => (
                    <Badge
                      key={skill}
                      variant={selectedSkills.includes(skill) ? "default" : "outline"}
                      className={selectedSkills.includes(skill)
                        ? "bg-pink-500 hover:bg-pink-600 cursor-pointer"
                        : "bg-zinc-800 hover:bg-zinc-700 cursor-pointer"}
                      onClick={() => toggleSkill(skill)}
                    >
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>

            {/* Main grid */}
            <div className="lg:col-span-3">
              {loading ? (
                <div className="flex justify-center py-16">
                  <div className="w-7 h-7 border-2 border-pink-500 border-t-transparent rounded-full animate-spin" />
                </div>
              ) : filteredMembers.length > 0 ? (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {filteredMembers.map(member => (
                      <TeamMemberCard key={member.roll_no} member={member} />
                    ))}
                  </div>

                  {/* Sentinel */}
                  <div ref={sentinelRef} className="h-10" />

                  {loadingMore && (
                    <div className="flex justify-center py-6">
                      <div className="w-6 h-6 border-2 border-pink-500 border-t-transparent rounded-full animate-spin" />
                    </div>
                  )}
                </>
              ) : (
                <div className="flex flex-col items-center justify-center py-16 bg-zinc-900 rounded-lg border border-zinc-800">
                  <p className="text-zinc-500">No team members match your search criteria</p>
                  <Button variant="outline" className="mt-4" onClick={clearSearch}>
                    Clear Filters
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
