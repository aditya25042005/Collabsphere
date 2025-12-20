"use client"

import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import TeamMemberCard from "@/components/team-member-card"
import { teamMembersData } from "@/lib/sample-data"
import { Search } from 'lucide-react'
//import APIBASE from './api.tsx'
export default function TeamPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedSkills, setSelectedSkills] = useState<string[]>([])
  
  // Get all unique skills from team members
  const allSkills = Array.from(
    new Set(
      teamMembersData.flatMap(member => member.skills)
    )
  ).sort()
  
  // Filter team members based on search query and selected skills
  const filteredMembers = teamMembersData.filter(member => {
    const matchesSearch = 
      searchQuery === "" || 
      member.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      member.role.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesSkills = 
      selectedSkills.length === 0 || 
      selectedSkills.every(skill => member.skills.includes(skill))
    
    return matchesSearch && matchesSkills
  })
  
  const toggleSkill = (skill: string) => {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(selectedSkills.filter(s => s !== skill))
    } else {
      setSelectedSkills([...selectedSkills, skill])
    }
  }
  
  return (
    <main className="min-h-screen bg-black text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-pink-500 mb-8">Team Members</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-8">
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-zinc-900 rounded-lg border border-zinc-800 p-4">
              <h2 className="text-lg font-semibold mb-4">Search</h2>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input 
                  placeholder="Search by name or role" 
                  className="pl-9 bg-zinc-800 border-zinc-700"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
            
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
          
          <div className="lg:col-span-3">
            {filteredMembers.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {filteredMembers.map(member => (
                  <TeamMemberCard key={member.id} member={member} />
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-16 bg-zinc-900 rounded-lg border border-zinc-800">
                <p className="text-muted-foreground">No team members match your search criteria</p>
                <Button 
                  variant="outline" 
                  className="mt-4"
                  onClick={() => {
                    setSearchQuery("")
                    setSelectedSkills([])
                  }}
                >
                  Clear Filters
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}