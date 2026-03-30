import search from '@inquirer/search'
import * as p from '@clack/prompts'

p.intro('My CLI')

const choice = await search({
  message: 'Pick a country',
  source: async (input) => {
    const options = ['Costa Rica', 'Mexico', 'Brazil', 'Argentina', /* ...100 more */]
    if (!input) return options.map(o => ({ name: o, value: o }))
    return options
      .filter(o => o.toLowerCase().includes(input.toLowerCase()))
      .map(o => ({ name: o, value: o }))
  }
})

p.outro(`You picked ${choice}`)