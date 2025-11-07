<template>
    <div class="min-h-screen bg-background text-foreground p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold mb-2">Fermentable Inventory</h1>
                <p class="text-muted-foreground">Manage your grains, extracts, and sugars</p>
            </div>
            <Button @click="showAddDialog = true" class="bg-primary hover:bg-primary/90">
                <Plus class="mr-2 h-4 w-4" />
                Add Fermentable
            </Button>
        </div>

        <!-- Search and Filter -->
        <div class="flex gap-4 mb-6">
            <div class="flex-1">
                <Input v-model="searchQuery" placeholder="Search fermentables by name, type, origin..."
                    class="bg-card border-input" />
            </div>
            <Select v-model="filterType">
                <SelectTrigger class="w-[180px] bg-card border-input">
                    <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="grain">Grain</SelectItem>
                    <SelectItem value="extract">Extract</SelectItem>
                    <SelectItem value="sugar">Sugar</SelectItem>
                </SelectContent>
            </Select>
        </div>

        <!-- Loading State -->
        <div v-if="fermentablesLoading" class="flex justify-center items-center py-12">
            <div class="text-muted-foreground">Loading fermentables inventory...</div>
        </div>

        <!-- Error State -->
        <div v-else-if="fermentablesError"
            class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded">
            <p class="font-bold">Error loading fermentables</p>
            <p>{{ fermentablesError }}</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredFermentables.length === 0 && !searchQuery"
            class="text-center py-12 bg-card rounded-lg border border-border">
            <Package class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 class="text-lg font-semibold mb-2">No fermentables in inventory</h3>
            <p class="text-muted-foreground mb-4">Start by adding your first fermentable</p>
            <Button @click="showAddDialog = true" class="bg-primary hover:bg-primary/90">
                <Plus class="mr-2 h-4 w-4" />
                Add First Fermentable
            </Button>
        </div>

        <!-- Fermentables Table -->
        <div v-else class="bg-card rounded-lg border border-border overflow-hidden">
            <Table>
                <TableHeader>
                    <TableRow class="hover:bg-transparent border-border">
                        <TableHead>Name</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Color (EBC)</TableHead>
                        <TableHead>Amount</TableHead>
                        <TableHead>Yield %</TableHead>
                        <TableHead>Origin</TableHead>
                        <TableHead>Supplier</TableHead>
                        <TableHead>Cost/Unit</TableHead>
                        <TableHead class="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow v-for="ferm in filteredFermentables" :key="ferm.id"
                        class="border-border hover:bg-accent/50"
                        :class="{ 'bg-destructive/10': isLowStock(ferm.amount) }">
                        <TableCell class="font-medium">{{ ferm.name }}</TableCell>
                        <TableCell>
                            <Badge variant="outline">{{ ferm.type }}</Badge>
                        </TableCell>
                        <TableCell>
                            <div class="flex items-center gap-2">
                                <div class="w-6 h-6 rounded border border-border"
                                    :style="{ backgroundColor: srmToRgb(ebcToSrm(ferm.color)) }"></div>
                                {{ ferm.color?.toFixed(0) || 'N/A' }}
                            </div>
                        </TableCell>
                        <TableCell>
                            <span :class="{ 'text-destructive font-bold': isLowStock(ferm.amount) }">
                                {{ ferm.amount }} {{ ferm.unit }}
                            </span>
                        </TableCell>
                        <TableCell>{{ ferm.yield_potential?.toFixed(1) || 'N/A' }}%</TableCell>
                        <TableCell>{{ ferm.origin || 'N/A' }}</TableCell>
                        <TableCell>{{ ferm.supplier || 'N/A' }}</TableCell>
                        <TableCell>
                            {{ ferm.cost_per_unit ? `€${ferm.cost_per_unit.toFixed(2)}` : 'N/A' }}
                        </TableCell>
                        <TableCell class="text-right">
                            <div class="flex justify-end gap-2">
                                <Button variant="ghost" size="sm" @click="editFermentable(ferm)">
                                    <Edit class="h-4 w-4" />
                                </Button>
                                <Button variant="ghost" size="sm" @click="confirmDelete(ferm)"
                                    class="text-destructive hover:text-destructive hover:bg-destructive/10">
                                    <Trash2 class="h-4 w-4" />
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>

        <!-- Summary Stats -->
        <div v-if="fermentables.length > 0" class="grid grid-cols-4 gap-4 mt-6">
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Items</div>
                <div class="text-2xl font-bold">{{ fermentables.length }}</div>
            </div>
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Low Stock Items</div>
                <div class="text-2xl font-bold text-destructive">{{ lowStockCount }}</div>
            </div>
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Value</div>
                <div class="text-2xl font-bold">€{{ totalValue.toFixed(2) }}</div>
            </div>
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Weight</div>
                <div class="text-2xl font-bold">{{ totalWeight.toFixed(2) }} kg</div>
            </div>
        </div>

        <!-- Add/Edit Dialog -->
        <Dialog v-model:open="showAddDialog">
            <DialogContent class="bg-card border-border max-w-2xl">
                <DialogHeader>
                    <DialogTitle>{{ editingFermentable ? 'Edit Fermentable' : 'Add New Fermentable' }}</DialogTitle>
                </DialogHeader>
                <div class="grid grid-cols-2 gap-4 py-4">
                    <div class="col-span-2">
                        <Label for="name">Name *</Label>
                        <Input id="name" v-model="formData.name" placeholder="e.g., Pilsner Malt"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="type">Type *</Label>
                        <Select v-model="formData.type">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="grain">Grain</SelectItem>
                                <SelectItem value="extract">Extract</SelectItem>
                                <SelectItem value="sugar">Sugar</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="color">Color (EBC) *</Label>
                        <Input id="color" v-model.number="formData.color" type="number" step="0.1"
                            placeholder="e.g., 3.5" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="amount">Amount *</Label>
                        <Input id="amount" v-model.number="formData.amount" type="number" step="0.1"
                            placeholder="e.g., 25" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="unit">Unit *</Label>
                        <Select v-model="formData.unit">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select unit" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="g">Grams (g)</SelectItem>
                                <SelectItem value="kg">Kilograms (kg)</SelectItem>
                                <SelectItem value="oz">Ounces (oz)</SelectItem>
                                <SelectItem value="lb">Pounds (lb)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="yield_potential">Yield Potential (%)</Label>
                        <Input id="yield_potential" v-model.number="formData.yield_potential" type="number" step="0.1"
                            placeholder="e.g., 80" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="origin">Origin</Label>
                        <Input id="origin" v-model="formData.origin" placeholder="e.g., Germany"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="supplier">Supplier</Label>
                        <Input id="supplier" v-model="formData.supplier" placeholder="e.g., BrewStore"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="cost_per_unit">Cost per Unit (€)</Label>
                        <Input id="cost_per_unit" v-model.number="formData.cost_per_unit" type="number" step="0.01"
                            placeholder="e.g., 2.50" class="bg-background border-input" />
                    </div>

                    <div class="col-span-2">
                        <Label for="notes">Notes</Label>
                        <Textarea id="notes" v-model="formData.notes" placeholder="Additional notes..."
                            class="bg-background border-input" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Cancel</Button>
                    <Button @click="saveFermentable" :disabled="!isFormValid" class="bg-primary hover:bg-primary/90">
                        {{ editingFermentable ? 'Update' : 'Add' }} Fermentable
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Plus, Edit, Trash2, Package } from 'lucide-vue-next'
import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Label } from '~/components/ui/label'
import { Textarea } from '~/components/ui/textarea'
import { Badge } from '~/components/ui/badge'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '~/components/ui/table'
import {
    Dialog,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '~/components/ui/dialog'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '~/components/ui/select'
import type { InventoryFermentable } from '~/composables/useInventory'

const {
    fermentables,
    fermentablesLoading,
    fermentablesError,
    fetchFermentables,
    addFermentable,
    updateFermentable,
    removeFermentable
} = useInventory()

// Search and filter
const searchQuery = ref('')
const filterType = ref('all')

// Dialog state
const showAddDialog = ref(false)
const editingFermentable = ref<InventoryFermentable | null>(null)

// Form data
const formData = ref({
    name: '',
    type: 'grain',
    color: 0,
    amount: 0,
    unit: 'kg',
    yield_potential: 0,
    origin: '',
    supplier: '',
    cost_per_unit: 0,
    notes: '',
})

// Computed
const filteredFermentables = computed(() => {
    let filtered = fermentables.value

    // Filter by type
    if (filterType.value !== 'all') {
        filtered = filtered.filter(f => f.type === filterType.value)
    }

    // Filter by search
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(f =>
            f.name.toLowerCase().includes(query) ||
            f.origin?.toLowerCase().includes(query) ||
            f.type?.toLowerCase().includes(query) ||
            f.supplier?.toLowerCase().includes(query)
        )
    }

    return filtered
})

const lowStockCount = computed(() => {
    return fermentables.value.filter(f => isLowStock(f.amount)).length
})

const totalValue = computed(() => {
    return fermentables.value.reduce((total, f) => {
        return total + (f.cost_per_unit || 0) * f.amount
    }, 0)
})

const totalWeight = computed(() => {
    return fermentables.value.reduce((total, f) => {
        // Convert everything to kg
        let kg = f.amount
        if (f.unit === 'g') kg = f.amount / 1000
        else if (f.unit === 'lb') kg = f.amount * 0.453592
        else if (f.unit === 'oz') kg = f.amount * 0.0283495
        return total + kg
    }, 0)
})

const isFormValid = computed(() => {
    return formData.value.name &&
        formData.value.type &&
        formData.value.color >= 0 &&
        formData.value.amount > 0 &&
        formData.value.unit
})

// Methods
function isLowStock(amount: number): boolean {
    return amount < 1 // Less than 1 kg/lb
}

function ebcToSrm(ebc: number): number {
    return ebc * 0.508
}

function srmToRgb(srm: number): string {
    // SRM to RGB approximation for beer color
    const colors = [
        [255, 230, 153], [255, 216, 120], [255, 204, 102], [255, 191, 86],
        [251, 177, 70], [248, 166, 53], [239, 148, 37], [230, 138, 20],
        [216, 124, 15], [204, 113, 10], [197, 99, 8], [186, 87, 6],
        [173, 74, 4], [160, 65, 3], [140, 50, 2], [119, 41, 1],
        [104, 35, 1], [96, 28, 0], [89, 26, 0], [79, 23, 0],
        [74, 21, 0], [69, 19, 0], [63, 17, 0], [58, 16, 0],
        [54, 14, 0], [50, 13, 0], [46, 12, 0], [43, 11, 0],
        [40, 10, 0], [37, 9, 0], [35, 8, 0], [33, 7, 0],
        [30, 7, 0], [28, 6, 0], [27, 6, 0], [25, 5, 0],
        [24, 5, 0], [22, 4, 0], [21, 4, 0], [20, 4, 0]
    ]

    const index = Math.min(Math.floor(srm), colors.length - 1)
    const [r, g, b] = colors[index] || [0, 0, 0]
    return `rgb(${r}, ${g}, ${b})`
}

function editFermentable(fermentable: InventoryFermentable) {
    editingFermentable.value = fermentable
    formData.value = {
        name: fermentable.name,
        type: fermentable.type,
        color: fermentable.color,
        amount: fermentable.amount,
        unit: fermentable.unit,
        yield_potential: fermentable.yield_potential || 0,
        origin: fermentable.origin || '',
        supplier: fermentable.supplier || '',
        cost_per_unit: fermentable.cost_per_unit || 0,
        notes: fermentable.notes || '',
    }
    showAddDialog.value = true
}

async function saveFermentable() {
    if (!isFormValid.value) return

    if (editingFermentable.value) {
        await updateFermentable(editingFermentable.value.id, formData.value)
    } else {
        await addFermentable(formData.value)
    }

    cancelEdit()
}

function cancelEdit() {
    showAddDialog.value = false
    editingFermentable.value = null
    formData.value = {
        name: '',
        type: 'grain',
        color: 0,
        amount: 0,
        unit: 'kg',
        yield_potential: 0,
        origin: '',
        supplier: '',
        cost_per_unit: 0,
        notes: '',
    }
}

async function confirmDelete(fermentable: InventoryFermentable) {
    if (confirm(`Are you sure you want to delete ${fermentable.name}?`)) {
        await removeFermentable(fermentable.id)
    }
}

// Lifecycle
onMounted(async () => {
    await fetchFermentables()
})
</script>
