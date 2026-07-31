import {useMemo,useState} from 'react'
import {BarChart3,BriefcaseBusiness,CalendarClock,ChevronDown,CircleUserRound,Command,LayoutDashboard,Plus,Search,Sparkles,Target,TrendingUp,X} from 'lucide-react'

type Stage='Wishlist'|'Applied'|'Interview'|'Offer'
type Job={id:number;company:string;role:string;location:string;stage:Stage;date:string;score:number;color:string}
const initial:Job[]=[
 {id:1,company:'Mosaic Labs',role:'Junior Backend Engineer',location:'Remote · EU',stage:'Interview',date:'Aug 05',score:92,color:'#6b4eff'},
 {id:2,company:'Northstar',role:'Software Engineer I',location:'Athens · Hybrid',stage:'Applied',date:'Jul 30',score:87,color:'#ff845e'},
 {id:3,company:'Vertex AI',role:'ML Platform Intern',location:'Remote',stage:'Applied',date:'Jul 28',score:84,color:'#1d9a78'},
 {id:4,company:'Brightside',role:'Full-stack Developer',location:'Thessaloniki',stage:'Wishlist',date:'Jul 26',score:78,color:'#e6b13f'},
 {id:5,company:'Cloudnine',role:'Graduate Java Engineer',location:'Athens',stage:'Offer',date:'Jul 22',score:95,color:'#2f75d7'}
]
const stages:Stage[]=['Wishlist','Applied','Interview','Offer']
function App(){
 const [jobs,setJobs]=useState<Job[]>(initial)
 const [query,setQuery]=useState('')
 const [modal,setModal]=useState(false)
 const [active,setActive]=useState<Job>(initial[0])
 const [newJob,setNewJob]=useState({company:'',role:'',location:'Remote',stage:'Wishlist' as Stage})
 const visible=useMemo(()=>jobs.filter(j=>(j.company+' '+j.role).toLowerCase().includes(query.toLowerCase())),[jobs,query])
 const add=()=>{if(!newJob.company||!newJob.role)return;const job:Job={id:Date.now(),...newJob,date:'Today',score:82,color:'#6b4eff'};setJobs([job,...jobs]);setActive(job);setModal(false);setNewJob({company:'',role:'',location:'Remote',stage:'Wishlist'})}
 const count=(s:Stage)=>jobs.filter(j=>j.stage===s).length
 return <div className="appShell">
  <aside className="sidebar"><div className="logo"><Command size={19}/><span>careerflow</span></div><nav><a className="active"><LayoutDashboard/>Overview</a><a><BriefcaseBusiness/>Applications<span>{jobs.length}</span></a><a><CalendarClock/>Interviews<span>{count('Interview')}</span></a><a><BarChart3/>Insights</a></nav><div className="sidebarTip"><Sparkles/><b>AI career coach</b><p>Get tailored next steps from your pipeline.</p><button>Open coach</button></div><div className="profile"><div>GK</div><span><b>Georgios K.</b><small>Developer plan</small></span><ChevronDown/></div></aside>
  <main><header><div><small>MONDAY, 03 AUGUST</small><h1>Good morning, Georgios.</h1></div><div className="headerActions"><button className="searchToggle"><Search/></button><button className="addButton" onClick={()=>setModal(true)}><Plus/>Add application</button><CircleUserRound/></div></header>
   <section className="heroCard"><div><small>THIS WEEK'S FOCUS</small><h2>Turn your next interview<br/>into an offer.</h2><p>You have one interview coming up. CareerFlow prepared a focused checklist based on the role.</p><button><Sparkles/>View interview prep</button></div><div className="heroVisual"><div className="orbit o1"/><div className="orbit o2"/><Target/><span className="chip c1">System design</span><span className="chip c2">Spring Boot</span><span className="chip c3">Behavioural</span></div></section>
   <section className="stats"><article><span>Active applications</span><b>{jobs.length}</b><small><TrendingUp/>+2 this week</small></article><article><span>Response rate</span><b>42%</b><small className="neutral">Top 18% of candidates</small></article><article><span>Interviews</span><b>{count('Interview')}</b><small><TrendingUp/>One upcoming</small></article><article><span>Average fit score</span><b>{Math.round(jobs.reduce((a,j)=>a+j.score,0)/jobs.length)}%</b><small className="neutral">Strong alignment</small></article></section>
   <section className="workspace"><div className="pipeline"><div className="sectionTitle"><div><small>YOUR PIPELINE</small><h3>Applications</h3></div><label><Search/><input aria-label="Search applications" placeholder="Search" value={query} onChange={e=>setQuery(e.target.value)}/></label></div><div className="stageTabs">{stages.map(s=><button key={s}>{s}<span>{count(s)}</span></button>)}</div><div className="jobList">{visible.map(job=><button key={job.id} className={active.id===job.id?'selected':''} onClick={()=>setActive(job)}><i style={{background:job.color}}>{job.company[0]}</i><span><b>{job.role}</b><small>{job.company} · {job.location}</small></span><em>{job.stage}</em><time>{job.date}</time></button>)}</div></div>
    <aside className="detail"><div className="fit"><div className="fitRing" style={{'--score':`${active.score*3.6}deg`} as React.CSSProperties}><b>{active.score}%</b></div><span><small>RESUME FIT</small><b>Excellent match</b></span></div><h3>{active.role}</h3><p>{active.company} · {active.location}</p><div className="match"><small>TOP MATCHES</small><ul><li>REST API design <b>96%</b></li><li>Python / Java <b>91%</b></li><li>SQL databases <b>88%</b></li></ul></div><div className="next"><small>NEXT BEST ACTION</small><b>Personalize your opening summary</b><p>Highlight your production API and stance detection work.</p><button>Generate suggestion <Sparkles/></button></div></aside>
   </section>
  </main>
  {modal&&<div className="modalBack" onClick={()=>setModal(false)}><div className="modal" onClick={e=>e.stopPropagation()}><button className="close" onClick={()=>setModal(false)}><X/></button><small>NEW OPPORTUNITY</small><h2>Add an application</h2><p>Keep every role and next step in one place.</p><label>Company<input value={newJob.company} onChange={e=>setNewJob({...newJob,company:e.target.value})} placeholder="e.g. Acme"/></label><label>Role<input value={newJob.role} onChange={e=>setNewJob({...newJob,role:e.target.value})} placeholder="e.g. Backend Engineer"/></label><label>Location<input value={newJob.location} onChange={e=>setNewJob({...newJob,location:e.target.value})}/></label><label>Stage<select value={newJob.stage} onChange={e=>setNewJob({...newJob,stage:e.target.value as Stage})}>{stages.map(s=><option key={s}>{s}</option>)}</select></label><button className="save" onClick={add}>Save application</button></div></div>}
 </div>
}
export default App
