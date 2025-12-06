<template>
    <div class="min-h-screen bg-background text-foreground p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold mb-2">Miscellaneous Inventory</h1>
                <p class="text-muted-foreground">Manage spices, finings, water agents, and other additives</p>
            </div>
            <Button class="bg-primary hover:bg-primary/90" @click="showAddDialog = true">
                <Plus class="mr-2 h-4 w-4" />
                Add Misc Item
            </Button>
        </div>

        <!-- Search and Filter -->
        <div class="flex gap-4 mb-6">
            <div class="flex-1">
                <Input
v-model="searchQuery" placeholder="Search miscellaneous items by name, type, use..."
                    class="bg-card border-input" />
            </div>
            <Select v-model="filterType">
                <SelectTrigger class="w-[200px] bg-card border-input">
                    <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="spice">Spice</SelectItem>
                    <SelectItem value="fining">Fining</SelectItem>
                    <SelectItem value="water agent">Water Agent</SelectItem>
                    <SelectItem value="herb">Herb</SelectItem>
                    <SelectItem value="flavor">Flavor</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                </SelectContent>
            </Select>
        </div>

        <!-- Loading State -->
        <div v-if="miscsLoading" class="flex justify-center items-center py-12">
            <div class="text-muted-foreground">Loading miscellaneous inventory...</div>
        </div>

        <!-- Error State -->
        <div
v-else-if="miscsError"
            class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded">
            <p class="font-bold">Error loading miscellaneous items</p>
            <p>{{ miscsError }}</p>
        </div>

        <!-- Empty State -->
        <div
v-else-if="filteredMiscs.length === 0 && !searchQuery"
            class="text-center py-12 bg-card rounded-lg border border-border">
            <Package class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 class="text-lg font-semibold mb-2">No miscellaneous items in inventory</h3>
            <p class="text-muted-foreground mb-4">Start by adding your first item</p>
            <Button class="bg-primary hover:bg-primary/90" @click="showAddDialog = true">
                <Plus class="mr-2 h-4 w-4" />
                Add First Item
            </Button>
        </div>

        <!-- Miscs Table -->
        <div v-else class="bg-card rounded-lg border border-border overflow-hidden">
            <Table>
                <TableHeader>
                    <TableRow class="hover:bg-transparent border-border">
                        <TableHead>Name</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Use</TableHead>
                        <TableHead>Amount</TableHead>
                        <TableHead>Use For</TableHead>
                        <TableHead>Supplier</TableHead>
                        <TableHead>Cost/Unit</TableHead>
                        <TableHead class="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow
v-for="misc in filteredMiscs" :key="misc.id" class="border-border hover:bg-accent/50"
                        :class="{ 'bg-destructive/10': isLowStock(misc.amount) }">
                        <TableCell class="font-medium">{{ misc.name }}</TableCell>
                        <TableCell>
                            <Badge variant="outline">{{ misc.type }}</Badge>
                        </TableCell>
                        <TableCell>
                            <Badge variant="secondary">{{ misc.use }}</Badge>
                        </TableCell>
                        <TableCell>
                            <span :class="{ 'text-destructive font-bold': isLowStock(misc.amount) }">
                                {{ misc.amount }} {{ misc.unit }}
                            </span>
                        </TableCell>
                        <TableCell>
                            <span class="text-sm text-muted-foreground">{{ misc.use_for || 'N/A' }}</span>
                        </TableCell>
                        <TableCell>{{ misc.supplier || 'N/A' }}</TableCell>
                        <TableCell>
                            {{ misc.cost_per_unit ? `€${misc.cost_per_unit.toFixed(2)}` : 'N/A' }}
                        </TableCell>
                        <TableCell class="text-right">
                            <div class="flex justify-end gap-2">
                                <Button variant="ghost" size="sm" @click="editMisc(misc)">
                                    <Edit class="h-4 w-4" />
                                </Button>
                                <Button
variant="ghost" size="sm" class="text-destructive hover:text-destructive hover:bg-destructive/10"
                                    @click="confirmDelete(misc)">
                                    <Trash2 class="h-4 w-4" />
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>

        <!-- Summary Stats -->
        <div v-if="miscs.length > 0" class="grid grid-cols-4 gap-4 mt-6">
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Items</div>
                <div class="text-2xl font-bold">{{ miscs.length }}</div>
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
                <div class="text-sm text-muted-foreground">Item Types</div>
                <div class="text-2xl font-bold">{{ uniqueTypes }}</div>
            </div>
        </div>

        <!-- Add/Edit Dialog -->
        <Dialog v-model:open="showAddDialog">
            <DialogContent class="bg-card border-border max-w-2xl">
                <DialogHeader>
                    <DialogTitle>{{ editingMisc ? 'Edit Miscellaneous Item' : 'Add New Miscellaneous Item' }}
                    </DialogTitle>
                </DialogHeader>
                <div class="grid grid-cols-2 gap-4 py-4">
                    <div class="col-span-2">
                        <Label for="name">Name *</Label>
                        <Input
id="name" v-model="formData.name" placeholder="e.g., Irish Moss"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="type">Type *</Label>
                        <Select v-model="formData.type">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="spice">Spice</SelectItem>
                                <SelectItem value="fining">Fining</SelectItem>
                                <SelectItem value="water agent">Water Agent</SelectItem>
                                <SelectItem value="herb">Herb</SelectItem>
                                <SelectItem value="flavor">Flavor</SelectItem>
                                <SelectItem value="other">Other</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="use">Use *</Label>
                        <Select v-model="formData.use">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select use" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="boil">Boil</SelectItem>
                                <SelectItem value="mash">Mash</SelectItem>
                                <SelectItem value="primary">Primary</SelectItem>
                                <SelectItem value="secondary">Secondary</SelectItem>
                                <SelectItem value="bottling">Bottling</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="amount">Amount *</Label>
                        <Input
id="amount" v-model.number="formData.amount" type="number" step="0.1"
                            placeholder="e.g., 100" class="bg-background border-input" />
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
                                <SelectItem value="ml">Milliliters (ml)</SelectItem>
                                <SelectItem value="l">Liters (l)</SelectItem>
                                <SelectItem value="tsp">Teaspoon (tsp)</SelectItem>
                                <SelectItem value="tbsp">Tablespoon (tbsp)</SelectItem>
                                <SelectItem value="items">Items</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div class="col-span-2">
                        <Label for="use_for">Use For</Label>
                        <Input
id="use_for" v-model="formData.use_for"
                            placeholder="e.g., Clarity, pH adjustment, flavor" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="supplier">Supplier</Label>
                        <Input
id="supplier" v-model="formData.supplier" placeholder="e.g., BrewStore"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="cost_per_unit">Cost per Unit (€)</Label>
                        <Input
id="cost_per_unit" v-model.number="formData.cost_per_unit" type="number" step="0.01"
                            placeholder="e.g., 0.10" class="bg-background border-input" />
                    </div>

                    <div class="col-span-2">
                        <Label for="notes">Notes</Label>
                        <Textarea
id="notes" v-model="formData.notes" placeholder="Additional notes..."
                            class="bg-background border-input" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Cancel</Button>
                    <Button :disabled="!isFormValid" class="bg-primary hover:bg-primary/90" @click="saveMisc">
                        {{ editingMisc ? 'Update' : 'Add' }} Item
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
import type { InventoryMisc } from '~/composables/useInventory'

const {
    miscs,
    miscsLoading,
    miscsError,
    fetchMiscs,
    addMisc,
    updateMisc,
    removeMisc
} = useInventory()

// Search and filter
const searchQuery = ref('')
const filterType = ref('all')

// Dialog state
const showAddDialog = ref(false)
const editingMisc = ref<InventoryMisc | null>(null)

// Form data
const formData = ref({
    name: '',
    type: 'spice',
    use: 'boil',
    amount: 0,
    unit: 'g',
    use_for: '',
    supplier: '',
    cost_per_unit: 0,
    notes: '',
})

// Computed
const filteredMiscs = computed(() => {
    let filtered = miscs.value

    // Filter by type
    if (filterType.value !== 'all') {
        filtered = filtered.filter(m => m.type === filterType.value)
    }

    // Filter by search
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(m =>
            m.name.toLowerCase().includes(query) ||
            m.type?.toLowerCase().includes(query) ||
            m.use?.toLowerCase().includes(query) ||
            m.use_for?.toLowerCase().includes(query) ||
            m.supplier?.toLowerCase().includes(query)
        )
    }

    return filtered
})

const lowStockCount = computed(() => {
    return miscs.value.filter(m => isLowStock(m.amount)).length
})

const totalValue = computed(() => {
    return miscs.value.reduce((total, m) => {
        return total + (m.cost_per_unit || 0) * m.amount
    }, 0)
})

const uniqueTypes = computed(() => {
    const types = new Set(miscs.value.map(m => m.type))
    return types.size
})

const isFormValid = computed(() => {
    return formData.value.name &&
        formData.value.type &&
        formData.value.use &&
        formData.value.amount > 0 &&
        formData.value.unit
})

// Methods
function isLowStock(amount: number): boolean {
    return amount < 10 // Less than 10 units (context dependent)
}

function editMisc(misc: InventoryMisc) {
    editingMisc.value = misc
    formData.value = {
        name: misc.name,
        type: misc.type,
        use: misc.use,
        amount: misc.amount,
        unit: misc.unit,
        use_for: misc.use_for || '',
        supplier: misc.supplier || '',
        cost_per_unit: misc.cost_per_unit || 0,
        notes: misc.notes || '',
    }
    showAddDialog.value = true
}

async function saveMisc() {
    if (!isFormValid.value) return

    if (editingMisc.value) {
        await updateMisc(editingMisc.value.id, formData.value)
    } else {
        await addMisc(formData.value)
    }

    cancelEdit()
}

function cancelEdit() {
    showAddDialog.value = false
    editingMisc.value = null
    formData.value = {
        name: '',
        type: 'spice',
        use: 'boil',
        amount: 0,
        unit: 'g',
        use_for: '',
        supplier: '',
        cost_per_unit: 0,
        notes: '',
    }
}

async function confirmDelete(misc: InventoryMisc) {
    if (confirm(`Are you sure you want to delete ${misc.name}?`)) {
        await removeMisc(misc.id)
    }
}

// Lifecycle
onMounted(async () => {
    await fetchMiscs()
})
</script>
