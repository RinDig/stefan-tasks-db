import asyncio
import httpx
from datetime import datetime, timedelta
import uuid

# Use the deployed backend URL for seeding
import sys
API_URL = sys.argv[1] if len(sys.argv) > 1 else "https://stefan-tasks-db.onrender.com"
print(f"Seeding data to: {API_URL}")

# Stefan's real task data
INITIAL_TASKS = [
    # Backlog tasks
    {
        "title": "Victor: Shop blasting projects through year-end",
        "category": "planning",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "Victor",
            "notes": "Monday meeting - Dates, sqft, pricing",
            "emoji": "📅"
        }
    },
    {
        "title": "US Soccer: Plan remaining jobs through Summer 2025",
        "category": "planning",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "US Soccer",
            "notes": "Material needs assessment",
            "emoji": "📋"
        }
    },
    {
        "title": "Jerry Solomon: Schedule floor painting",
        "category": "customer",
        "priority": "high",
        "column": "backlog",
        "metadata": {
            "client": "Jerry Solomon",
            "due_date": "2025-10-15",
            "notes": "Before Oct 15 warehouse deadline",
            "emoji": "⏰"
        }
    },
    {
        "title": "Jared (Sanford): Schedule basketball lines",
        "category": "customer",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "Jared (Sanford)",
            "notes": "Court marking",
            "emoji": "🏀"
        }
    },
    {
        "title": "Pastor Tom: Schedule West Oaks touch-ups",
        "category": "customer",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "Pastor Tom",
            "notes": "Maintenance work",
            "emoji": "🎨"
        }
    },
    {
        "title": "Coastal Construction: Get start/finish dates",
        "category": "concrete",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "Coastal Construction",
            "notes": "Schedule coordination",
            "emoji": "📅"
        }
    },
    {
        "title": "DACG: Harbor Island Side 1 pour dates",
        "category": "concrete",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "DACG",
            "notes": "Hotels needed, Materials to order",
            "emoji": "🏗️"
        }
    },
    {
        "title": "Pickle Tile: Winter Springs project details",
        "category": "customer",
        "priority": "normal",
        "column": "backlog",
        "metadata": {
            "client": "Pickle Tile",
            "notes": "Check warehouse materials",
            "emoji": "📦"
        }
    },
    
    # This Week tasks
    {
        "title": "Drew/US Soccer: Review 7 NYC repair jobs & respond",
        "category": "customer",
        "priority": "urgent",
        "column": "this-week",
        "metadata": {
            "client": "Drew/US Soccer",
            "due_date": str(datetime.now().date()),
            "notes": "Check photos, Verify storage materials, EOD deadline",
            "emoji": "🔥"
        }
    },
    {
        "title": "DACG Concrete: Get Georgia job start date",
        "category": "concrete",
        "priority": "urgent",
        "column": "this-week",
        "metadata": {
            "client": "DACG Concrete",
            "due_date": str(datetime.now().date()),
            "notes": "Call required, Crew assignment pending",
            "emoji": "🔥"
        }
    },
    {
        "title": "John Casey (Boston): Notify 5-day delay, new start 26th",
        "category": "customer",
        "priority": "urgent",
        "column": "this-week",
        "metadata": {
            "client": "John Casey (Boston)",
            "due_date": str(datetime.now().date()),
            "notes": "Shipment delayed, Customer notification",
            "emoji": "🔥"
        }
    },
    {
        "title": "Kentucky Crew: Replace Kevin, determine who to send",
        "category": "crew",
        "priority": "high",
        "column": "this-week",
        "metadata": {
            "client": "Kentucky Crew",
            "notes": "Weather concerns, Talk to Kyle & Dad",
            "emoji": "⚡"
        }
    },
    {
        "title": "Schedule Monday pickup for Asheville portable floor",
        "category": "materials",
        "priority": "high",
        "column": "this-week",
        "metadata": {
            "notes": "Kelly coordination, Packing required",
            "emoji": "⚡"
        }
    },
    {
        "title": "Create & send 2-week schedule for all crews",
        "category": "crew",
        "priority": "high",
        "column": "this-week",
        "metadata": {
            "notes": "Day-by-day planning, Everything changed today",
            "emoji": "⚡"
        }
    },
    {
        "title": "Lifetime Warner Park: Reject forced schedule, negotiate dates",
        "category": "customer",
        "priority": "normal",
        "column": "this-week",
        "metadata": {
            "client": "Lifetime Warner Park",
            "notes": "Schedule conflict",
            "emoji": "⏰"
        }
    },
    {
        "title": "Quality Contractor: Confirm TBOR Phase 2 - Aug 25 start",
        "category": "customer",
        "priority": "normal",
        "column": "this-week",
        "metadata": {
            "client": "Quality Contractor",
            "notes": "Start confirmation",
            "emoji": "📅"
        }
    },
    {
        "title": "Lifetime Fitness Casey: Confirm Sept 4 delivery",
        "category": "materials",
        "priority": "normal",
        "column": "this-week",
        "metadata": {
            "client": "Lifetime Fitness Casey",
            "notes": "Kelly coordination, Delivery confirmation",
            "emoji": "📦"
        }
    },
    {
        "title": "Kyle: Howard Middle School conflict with Lifetime projects",
        "category": "internal",
        "priority": "high",
        "column": "this-week",
        "metadata": {
            "client": "Kyle",
            "notes": "Booked 6 months ago, Major conflict",
            "emoji": "⚡"
        }
    },
    
    # In Progress tasks
    {
        "title": "Pack/organize Asheville shipment (avoid wrong floor)",
        "category": "materials",
        "priority": "normal",
        "column": "in-progress",
        "metadata": {
            "notes": "In progress, Check portable flooring",
            "emoji": "📦"
        }
    },
    {
        "title": "Barry Gladstone: Arranging materials, hotels, Labor Ready",
        "category": "customer",
        "priority": "normal",
        "column": "in-progress",
        "metadata": {
            "client": "Barry Gladstone",
            "notes": "Hotels pending, Penske rental needed",
            "emoji": "🏨"
        }
    },
    {
        "title": "Josh: Getting October dates for planning",
        "category": "crew",
        "priority": "normal",
        "column": "in-progress",
        "metadata": {
            "client": "Josh",
            "notes": "Waiting on response",
            "emoji": "📅"
        }
    },
    {
        "title": "Asheville Events: Planning 42 guys deployment",
        "category": "crew",
        "priority": "high",
        "column": "in-progress",
        "metadata": {
            "client": "Asheville Events",
            "notes": "Mandatory dates, Large crew coordination",
            "emoji": "👷"
        }
    },
    {
        "title": "NYC Storage inventory for US Soccer repairs",
        "category": "materials",
        "priority": "normal",
        "column": "in-progress",
        "metadata": {
            "notes": "Checking availability",
            "emoji": "📦"
        }
    },
    
    # Done tasks
    {
        "title": "Brain dump completed - all tasks documented",
        "category": "internal",
        "priority": "normal",
        "column": "done",
        "metadata": {
            "notes": "25+ tasks captured",
            "emoji": "✅"
        }
    },
    {
        "title": "Task board system implemented",
        "category": "internal",
        "priority": "normal",
        "column": "done",
        "metadata": {
            "notes": "Ready to use",
            "emoji": "🎯"
        }
    }
]

async def seed_database():
    async with httpx.AsyncClient() as client:
        # First, clear existing tasks (optional)
        try:
            response = await client.get(f"{API_URL}/tasks")
            if response.status_code == 200:
                existing_tasks = response.json()
                for task in existing_tasks:
                    await client.delete(f"{API_URL}/tasks/{task['id']}")
                print(f"Cleared {len(existing_tasks)} existing tasks")
        except Exception as e:
            print(f"Could not clear existing tasks: {e}")
        
        # Add Stefan's real tasks
        created_count = 0
        for task_data in INITIAL_TASKS:
            # Generate a unique ID for each task
            task_data["id"] = str(uuid.uuid4())
            
            try:
                response = await client.post(
                    f"{API_URL}/tasks",
                    json=task_data
                )
                if response.status_code == 200:
                    created_count += 1
                    print(f"Created: {task_data['title'][:50]}...")
                else:
                    print(f"Failed to create: {task_data['title'][:50]}...")
            except Exception as e:
                print(f"Error creating task: {e}")
        
        print(f"\nSuccessfully seeded {created_count} tasks!")

if __name__ == "__main__":
    print("Seeding Stefan's task data...")
    asyncio.run(seed_database())