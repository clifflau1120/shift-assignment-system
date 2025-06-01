# Shift Assignment System

A constraint-based shift scheduling application designed specifically for my nurse friend working for an elderly home. This application helps create optimal shift schedules while respecting various constraints including worker preferences, time-off requests, consecutive shift limitations, and regulatory requirements.

## Features

### Standard Shift Types

- `MORNING` (Symbol: `A`, equivalent to 8 working hours) - a morning shift from 7:00 to 15:00.
- `AFTERNOON` (Symbol: `P`, equivalent to 8 working hours) - an afternoon shift from 14:00 to 22:00.
- `NIGHT` (Symbol: `N`, equivalent to 9 working hours) - a night shift from 22:00 to 07:00.
- `TIME_OFF` (Symbol: `_`, equivalent to 0 working hours) - a regular time-off.
- `ANNUAL_LEAVE`\* (Symbol: `AL`, equivalent to 8 working hours) - an annual leave.
- `BIRTHDAY_LEAVE` (Symbol: `BL`, equivalent to 8 working hours) - a birthday leave.
- `PUBLIC_HOLIDAY` (Symbol: `PH`, equivalent to 8 working hours) - a public holiday, a compensation leave or a carryover of the above from the previous schedule.

\* 7 Consecutive `ANNUAL_LEAVE`s are count together as 44 working hours as opposed to 56 hours.

## Non-standard Shift Types:

- `MORNING_SHORTENED` (Symbol: `7-2`, equivalent to 7 working hours) - a shortened morning shift from 7:00 to 14:00.
- `MORNING_EXTENDED` (Symbol: `7-4`, equivalent to 0 working hours) - an extended morning shift from 7:00 to 16:00.
- `AFTERNOON_SHORTENED` (Symbol: `2-9`, equivalent to 7 working hours) - a shortened afternoon shift from 14:00 to 21:00.
- `AFTERNOON_EXTENDED` (Symbol: `1-10`, equivalent to 9 working hours) - an extended shift from 13:00 to 22:00.

Each full-time worker is required to work 270 hours per scheduling period, i.e. 6 weeks. These non-standard shifts are used to satisfy this requirement when there is no optimal solution with standard shifts.

### Scheduling rules

Scheduling rules are implemented as hard constraints and soft constraints:

- **Daily Shift Assignment** - ensures each worker has exactly one shift assignment everyday
- **Service coverage** - ensures consistent coverage of care services
  - 3-4 workers during morning and afternoon shifts
  - 2 workers during night shifts
- **Working Hours Balancing**: Ensures full-time workers complete exactly 270 working hours per scheduling period
- **Leave management**
  - Annual leaves with special handling for 7 consecutive leaves
  - Birthday leaves
  - Public holidays, compensation leaves and carryovers from previous schedule or to next schedule
- **Recovery Management**:
  - Ensures workers get time-offs after night shifts
  - Limits consecutive night shifts to a maximum of 2 days
  - Limits consecutive working days to a maximum of 6 days
  - Forbids afternoon-to-morning shift transitions unless configured
- **Shift Distribution Control**:
  - Limits consecutive time-offs to a maximum of 2 days
  - Prioritize full-time workers
- **Worker Preference System**: Honors requested shifts and time-offs when possible
- **Constraint-Based Optimization**: Uses Google OR-Tools to generate optimal schedules that satisfy all hard constraints while minimizing penalties for soft constraints

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) - to manage Python dependencies
- [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) (Optional) - to manage Python versions and virtual environments

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:pyenv/pyenv-virtualenv.git
   cd shift-assignment-system
   ```

2. Setup the virutal environment and install the dependencies:

   ```bash
   make setup
   ```

### Running the shift scheduler

1. Create [a configuration file](#configuration)
2. Run the scheduler with your configuration:
   ```bash
   shift-scheduler run --config configurations/config.json
   ```
3. Find your generated schedule in the `outputs` directory (or wherever specified in your configuration)

## Configuration

Configuration is provided by JSON files; you can create one in `configurations/config.json`.

### Basic Structure

```json
{
  "start_date": "2025-05-26",
  "end_date": "2025-07-06",
  "io": {
    "output_directory": "outputs",
    "output_file_name": "SA %-d.%-m.%y Generated.csv"
  },
  "workers": {
    "worker_name": {
      "is_full_time": true,
      "accept_pa_shifts": false,
      "carryovers": 0,
      "requests": {
        "A": [],
        "P": [],
        "N": ["2025-06-02"],
        "_": ["2025-06-03"],
        "AL": [],
        "BL": [],
        "PH": []
      }
    }
    // More workers...
  }
}
```

### Configuration Options

#### Main Settings

- `start_date`: First day of the scheduling period (YYYY-MM-DD)
- `end_date`: Last day of the scheduling period (YYYY-MM-DD)

#### I/O Settings

- `output_directory`: Directory where schedule files will be saved
- `output_file_name`: Filename template for output files (using Python strftime syntax)

#### Worker Preferences

For each worker:

- `is_full_time`: Whether the worker is full-time (true) or part-time (false)
- `accept_pa_shifts`: Whether the worker can work a morning shift after an afternoon shift
- `carryovers`: Number of public holiday carryovers from previous schedules
- `requests`: Specific shift requests, with dates listed for each [shift type](#standard-shift-types)

## Commands

The application provides several command-line tools:

### Generate Schedule

```bash
shift-scheduler run --config <path-to-config-file>
```

### Generate a JSON schema of the configuration file

```bash
shift-scheduler config-schema > configurations/schema.json
```

### Show Version

```bash
shift-scheduler version
```

## TODO

- Include unit tests
- Set up GitHub Actions for automated code quality checks

## Versioning

This repository adopts date-based versioning.
