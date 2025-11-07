<template>
    <div class="min-h-screen bg-background text-foreground p-8">
        <!-- Header -->
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold mb-2">Hop Inventory</h1>
                <p class="text-muted-foreground">Manage your hop stock and track freshness</p>
            </div>
            <Button @click="showAddDialog = true" class="bg-primary hover:bg-primary/90">
                <Plus class="mr-2 h-4 w-4" />
                Add Hop
            </Button>
        </div>

        <!-- Search and Filter -->
        <div class="flex gap-4 mb-6">
            <div class="flex-1">
                <Input v-model="searchQuery" placeholder="Search hops by name, origin, type..."
                    class="bg-card border-input" />
            </div>
            <Select v-model="filterType">
                <SelectTrigger class="w-[180px] bg-card border-input">
                    <SelectValue placeholder="Filter by type" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="all">All Types</SelectItem>
                    <SelectItem value="pellet">Pellet</SelectItem>
                    <SelectItem value="leaf">Leaf</SelectItem>
                    <SelectItem value="plug">Plug</SelectItem>
                </SelectContent>
            </Select>
        </div>

        <!-- Loading State -->
        <div v-if="hopsLoading" class="flex justify-center items-center py-12">
            <div class="text-muted-foreground">Loading hops inventory...</div>
        </div>

        <!-- Error State -->
        <div v-else-if="hopsError"
            class="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded">
            <p class="font-bold">Error loading hops</p>
            <p>{{ hopsError }}</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredHops.length === 0 && !searchQuery"
            class="text-center py-12 bg-card rounded-lg border border-border">
            <Package class="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 class="text-lg font-semibold mb-2">No hops in inventory</h3>
            <p class="text-muted-foreground mb-4">Start by adding your first hop variety</p>
            <Button @click="showAddDialog = true" class="bg-primary hover:bg-primary/90">
                <Plus class="mr-2 h-4 w-4" />
                Add First Hop
            </Button>
        </div>

        <!-- Hops Table -->
        <div v-else class="bg-card rounded-lg border border-border overflow-hidden">
            <Table>
                <TableHeader>
                    <TableRow class="hover:bg-transparent border-border">
                        <TableHead>Name</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Alpha Acid %</TableHead>
                        <TableHead>Amount</TableHead>
                        <TableHead>Origin</TableHead>
                        <TableHead>Supplier</TableHead>
                        <TableHead>Cost/Unit</TableHead>
                        <TableHead>Expiry</TableHead>
                        <TableHead class="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow v-for="hop in filteredHops" :key="hop.id" class="border-border hover:bg-accent/50"
                        :class="{ 'bg-destructive/10': isLowStock(hop.amount) || isExpiringSoon(hop.expiry_date) }">
                        <TableCell class="font-medium">{{ hop.name }}</TableCell>
                        <TableCell>
                            <Badge variant="outline">{{ hop.type }}</Badge>
                        </TableCell>
                        <TableCell>{{ hop.alpha_acid?.toFixed(1) || 'N/A' }}%</TableCell>
                        <TableCell>
                            <span :class="{ 'text-destructive font-bold': isLowStock(hop.amount) }">
                                {{ hop.amount }} {{ hop.unit }}
                            </span>
                        </TableCell>
                        <TableCell>{{ hop.origin || 'N/A' }}</TableCell>
                        <TableCell>{{ hop.supplier || 'N/A' }}</TableCell>
                        <TableCell>
                            {{ hop.cost_per_unit ? `€${hop.cost_per_unit.toFixed(2)}` : 'N/A' }}
                        </TableCell>
                        <TableCell>
                            <span :class="{ 'text-destructive font-bold': isExpiringSoon(hop.expiry_date) }">
                                {{ hop.expiry_date ? formatDate(hop.expiry_date) : 'N/A' }}
                            </span>
                        </TableCell>
                        <TableCell class="text-right">
                            <div class="flex justify-end gap-2">
                                <Button variant="ghost" size="sm" @click="editHop(hop)">
                                    <Edit class="h-4 w-4" />
                                </Button>
                                <Button variant="ghost" size="sm" @click="confirmDelete(hop)"
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
        <div v-if="hops.length > 0" class="grid grid-cols-4 gap-4 mt-6">
            <div class="bg-card rounded-lg border border-border p-4">
                <div class="text-sm text-muted-foreground">Total Varieties</div>
                <div class="text-2xl font-bold">{{ hops.length }}</div>
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
                <div class="text-sm text-muted-foreground">Expiring Soon</div>
                <div class="text-2xl font-bold text-destructive">{{ expiringSoonCount }}</div>
            </div>
        </div>

        <!-- Add/Edit Dialog -->
        <Dialog v-model:open="showAddDialog">
            <DialogContent class="bg-card border-border max-w-2xl">
                <DialogHeader>
                    <DialogTitle>{{ editingHop ? 'Edit Hop' : 'Add New Hop' }}</DialogTitle>
                </DialogHeader>
                <div class="grid grid-cols-2 gap-4 py-4">
                    <div class="col-span-2">
                        <Label for="name">Name *</Label>
                        <Input id="name" v-model="formData.name" placeholder="e.g., Cascade"
                            class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="type">Type *</Label>
                        <Select v-model="formData.type">
                            <SelectTrigger class="bg-background border-input">
                                <SelectValue placeholder="Select type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="pellet">Pellet</SelectItem>
                                <SelectItem value="leaf">Leaf</SelectItem>
                                <SelectItem value="plug">Plug</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div>
                        <Label for="alpha_acid">Alpha Acid % *</Label>
                        <Input id="alpha_acid" v-model.number="formData.alpha_acid" type="number" step="0.1"
                            placeholder="e.g., 5.5" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="amount">Amount *</Label>
                        <Input id="amount" v-model.number="formData.amount" type="number" step="1"
                            placeholder="e.g., 500" class="bg-background border-input" />
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
                        <Label for="origin">Origin</Label>
                        <Input id="origin" v-model="formData.origin" placeholder="e.g., USA"
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
                            placeholder="e.g., 0.05" class="bg-background border-input" />
                    </div>

                    <div>
                        <Label for="expiry_date">Expiry Date</Label>
                        <Input id="expiry_date" v-model="formData.expiry_date" type="date"
                            class="bg-background border-input" />
                    </div>

                    <div class="col-span-2">
                        <Label for="notes">Notes</Label>
                        <Textarea id="notes" v-model="formData.notes" placeholder="Additional notes..."
                            class="bg-background border-input" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Cancel</Button>
                    <Button @click="saveHop" :disabled="!isFormValid" class="bg-primary hover:bg-primary/90">
                        {{ editingHop ? 'Update' : 'Add' }} Hop
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
import type { InventoryHop } from '~/composables/useInventory'

const {
    hops,
    hopsLoading,
    hopsError,
    fetchHops,
    addHop,
    updateHop,
    removeHop
} = useInventory()

// Search and filter
const searchQuery = ref('')
const filterType = ref('all')

// Dialog state
const showAddDialog = ref(false)
const editingHop = ref<InventoryHop | null>(null)

// Form data
const formData = ref({
    name: '',
    type: 'pellet',
    alpha_acid: 0,
    amount: 0,
    unit: 'g',
    origin: '',
    supplier: '',
    cost_per_unit: 0,
    expiry_date: '',
    notes: '',
})

// Computed
const filteredHops = computed(() => {
    let filtered = hops.value

    // Filter by type
    if (filterType.value !== 'all') {
        filtered = filtered.filter(h => h.type === filterType.value)
    }

    // Filter by search
    if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(h =>
            h.name.toLowerCase().includes(query) ||
            h.origin?.toLowerCase().includes(query) ||
            h.type?.toLowerCase().includes(query) ||
            h.supplier?.toLowerCase().includes(query)
        )
    }

    return filtered
})

const lowStockCount = computed(() => {
    return hops.value.filter(h => isLowStock(h.amount)).length
})

const expiringSoonCount = computed(() => {
    return hops.value.filter(h => isExpiringSoon(h.expiry_date)).length
})

const totalValue = computed(() => {
    return hops.value.reduce((total, h) => {
        return total + (h.cost_per_unit || 0) * h.amount
    }, 0)
})

const isFormValid = computed(() => {
    return formData.value.name &&
        formData.value.type &&
        formData.value.alpha_acid > 0 &&
        formData.value.amount > 0 &&
        formData.value.unit
})

// Methods
function isLowStock(amount: number): boolean {
    return amount < 100
}

function isExpiringSoon(expiryDate?: string): boolean {
    if (!expiryDate) return false
    const expiry = new Date(expiryDate)
    const today = new Date()
    const diffDays = Math.ceil((expiry.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
    return diffDays >= 0 && diffDays < 90 // Expiring within 90 days
}

function formatDate(dateString: string): string {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    })
}

function editHop(hop: InventoryHop) {
    editingHop.value = hop
    formData.value = {
        name: hop.name,
        type: hop.type,
        alpha_acid: hop.alpha_acid,
        amount: hop.amount,
        unit: hop.unit,
        origin: hop.origin || '',
        supplier: hop.supplier || '',
        cost_per_unit: hop.cost_per_unit || 0,
        expiry_date: hop.expiry_date || '',
        notes: hop.notes || '',
    }
    showAddDialog.value = true
}

async function saveHop() {
    if (!isFormValid.value) return

    if (editingHop.value) {
        await updateHop(editingHop.value.id, formData.value)
    } else {
        await addHop(formData.value)
    }

    cancelEdit()
}

function cancelEdit() {
    showAddDialog.value = false
    editingHop.value = null
    formData.value = {
        name: '',
        type: 'pellet',
        alpha_acid: 0,
        amount: 0,
        unit: 'g',
        origin: '',
        supplier: '',
        cost_per_unit: 0,
        expiry_date: '',
        notes: '',
    }
}

async function confirmDelete(hop: InventoryHop) {
    if (confirm(`Are you sure you want to delete ${hop.name}?`)) {
        await removeHop(hop.id)
    }
}

// Lifecycle
onMounted(async () => {
    await fetchHops()
})
</script>
