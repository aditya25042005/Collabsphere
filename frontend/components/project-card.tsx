import Link from "next/link"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Calendar, Users, Clock, ShieldCheck } from "lucide-react"
import { formatDistanceToNow } from "date-fns"


interface Project {
  admin_id: number
  admin_name?: string
  current_members?: number
  user_role?: string | null
  description: string
  project_id: number
  end_date: string
  members_required: number
  start_date: string
  status: string
  title: string
  tags: string
}


interface ProjectCardProps {
  project: Project

}

export default function ProjectCard({ project }: ProjectCardProps) {
  const { project_id, title, description, tags, start_date, end_date, members_required, current_members, status, admin_name, user_role } = project
  const tagArray = tags.split(",").map((tag) => tag.trim())

  // Calculate days remaining or days since completion
  const today = new Date()
  const end = new Date(end_date)
  const timeRemaining = formatDistanceToNow(end, { addSuffix: true })

  return (
    <Link href={`/project/${project_id}`}>
      <Card className="bg-zinc-900 border-zinc-800 hover:border-zinc-700 transition-all h-full flex flex-col">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-start">
            <CardTitle className="text-xl font-semibold text-white">{title}</CardTitle>
            <Badge
              variant="outline"
              className={
                user_role === "admin"
                  ? "bg-pink-500/10 text-pink-400 border-pink-500/20"
                  : user_role === "member"
                    ? "bg-blue-500/10 text-blue-400 border-blue-500/20"
                    : status === "Completed"
                      ? "bg-purple-500/10 text-purple-400 border-purple-500/20"
                      : status === "Applied"
                        ? "bg-green-500/10 text-green-400 border-green-500/20"
                        : "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
              }
            >
              {user_role === "admin"
                ? "Admin"
                : user_role === "member"
                  ? "Member"
                  : status === "Completed"
                    ? "Completed"
                    : status === "Applied"
                      ? "Applied"
                      : status}
            </Badge>
          </div>
          <p className="text-muted-foreground text-sm line-clamp-2 mt-1">{description}</p>
        </CardHeader>

        <CardContent className="py-2 flex-grow">
          <div className="flex flex-wrap gap-1 mb-4">
          {tagArray.map((tech, index) => (
              <Badge key={index} variant="secondary" className="bg-zinc-800">
                {tech}
              </Badge>
            ))}
          </div>

        </CardContent>

        <CardFooter className="pt-2 border-t border-zinc-800 flex flex-col space-y-2">
          <div className="flex justify-between w-full text-xs text-muted-foreground">
            <div className="flex items-center">
              <Calendar className="h-3 w-3 mr-1" />
              <span>{new Date(start_date).toLocaleDateString()}</span>
            </div>
            <div className="flex items-center">
              <Clock className="h-3 w-3 mr-1" />
              <span>{timeRemaining}</span>
            </div>
          </div>

          <div className="flex justify-between w-full text-xs text-muted-foreground">
            <div className="flex items-center">
              <Users className="h-3 w-3 mr-1" />
              <span>
                {current_members !== undefined
                  ? `${current_members}/${members_required} members`
                  : `${members_required} members`}
              </span>
            </div>
            {admin_name && (
              <div className="flex items-center gap-1">
                <ShieldCheck className="h-3 w-3 text-pink-400" />
                <span className="text-pink-400 font-medium">{admin_name}</span>
              </div>
            )}
          </div>
        </CardFooter>
      </Card>
    </Link>
  )
}

