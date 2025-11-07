export interface RecipeFixture {
  id: string
  name: string
  type: string
  brewer: string
  batch_size: number
  boil_size: number
  boil_time: number
  efficiency: number
}

export interface EquipmentFixture {
  id: number
  name: string
  description: string
  version: string
  batch_size: number
  boil_size: number
  tun_volume: number
  trub_chiller_loss: number
  lauter_deadspace: number
  top_up_water: number
  top_up_kettle: number
  hop_utilization: number
  boil_time: number
  calc_boil_volume: boolean
  tun_weight: number
  tun_specific_heat: number
  evap_rate: number
}

export const recipeFixtures: RecipeFixture[] = [
  {
    id: 'recipe-west-coast-ipa',
    name: 'West Coast IPA',
    type: 'IPA',
    brewer: 'Alex Brewer',
    batch_size: 19,
    boil_size: 25,
    boil_time: 60,
    efficiency: 72
  },
  {
    id: 'recipe-vienna-lager',
    name: 'Vienna Lager',
    type: 'Lager',
    brewer: 'Jamie Cellar',
    batch_size: 21,
    boil_size: 27,
    boil_time: 90,
    efficiency: 78
  },
  {
    id: 'recipe-stout',
    name: 'Midnight Stout',
    type: 'Stout',
    brewer: 'Morgan Dark',
    batch_size: 23,
    boil_size: 29,
    boil_time: 75,
    efficiency: 70
  }
]

export const equipmentFixtures: EquipmentFixture[] = [
  {
    id: 101,
    name: 'Brewzilla 65L System',
    description: 'Large batch electric system with recirculation',
    version: 'v2.1',
    batch_size: 25,
    boil_size: 30,
    tun_volume: 34,
    trub_chiller_loss: 1.2,
    lauter_deadspace: 2.2,
    top_up_water: 0,
    top_up_kettle: 0,
    hop_utilization: 96,
    boil_time: 60,
    calc_boil_volume: true,
    tun_weight: 12,
    tun_specific_heat: 0.38,
    evap_rate: 8
  },
  {
    id: 102,
    name: 'Anvil Foundry 10.5',
    description: 'Compact electric kettle for experimental batches',
    version: 'v1.5',
    batch_size: 12,
    boil_size: 15,
    tun_volume: 18,
    trub_chiller_loss: 0.8,
    lauter_deadspace: 1.5,
    top_up_water: 0,
    top_up_kettle: 0,
    hop_utilization: 92,
    boil_time: 70,
    calc_boil_volume: true,
    tun_weight: 8,
    tun_specific_heat: 0.35,
    evap_rate: 6
  }
]
