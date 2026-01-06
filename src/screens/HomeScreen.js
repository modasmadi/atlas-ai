import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, Alert, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Camera, FileText, Upload, Crown } from 'lucide-react-native';
import { COLORS, SPACING } from '../constants/theme';
import GradientButton from '../components/GradientButton';
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';

export default function HomeScreen({ navigation }) {
    const [dailyGenerations, setDailyGenerations] = useState(3);

    const pickImage = async () => {
        if (dailyGenerations <= 0) {
            navigation.navigate('Subscription');
            return;
        }

        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            quality: 1,
            base64: true,
        });

        if (!result.canceled) {
            setDailyGenerations(prev => prev - 1);
            navigation.navigate('Results', { type: 'image', uri: result.assets[0].uri });
        }
    };

    const pickDocument = async () => {
        if (dailyGenerations <= 0) {
            navigation.navigate('Subscription');
            return;
        }

        let result = await DocumentPicker.getDocumentAsync({
            type: 'application/pdf',
            copyToCacheDirectory: true,
        });

        if (!result.canceled) {
            setDailyGenerations(prev => prev - 1);
            navigation.navigate('Results', { type: 'document', uri: result.assets[0].uri, name: result.assets[0].name });
        }
    };

    return (
        <SafeAreaView style={styles.container}>
            <StatusBar style="light" />
            <View style={styles.header}>
                <View>
                    <Text style={styles.greeting}>Welcome back,</Text>
                    <Text style={styles.appName}>ATLAS AI</Text>
                </View>
                <TouchableOpacity
                    style={styles.premiumBadge}
                    onPress={() => navigation.navigate('Subscription')}
                >
                    <Crown size={20} color="#FFD700" />
                    <Text style={styles.premiumText}>Pro</Text>
                </TouchableOpacity>
            </View>

            <ScrollView contentContainerStyle={styles.content}>
                <View style={styles.statsCard}>
                    <Text style={styles.statsTitle}>Daily Credits</Text>
                    <Text style={styles.statsCount}>{dailyGenerations}/3</Text>
                    <View style={styles.progressBarBg}>
                        <View style={[styles.progressBarFill, { width: `${(dailyGenerations / 3) * 100}%` }]} />
                    </View>
                    <Text style={styles.resetText}>Resets in 14 hours</Text>
                </View>

                <Text style={styles.sectionTitle}>Quick Actions</Text>

                <View style={styles.grid}>
                    <TouchableOpacity style={styles.actionCard} onPress={pickImage}>
                        <View style={[styles.iconBox, { backgroundColor: 'rgba(59, 130, 246, 0.2)' }]}>
                            <Camera size={32} color={COLORS.primary} />
                        </View>
                        <Text style={styles.actionText}>Scan Question</Text>
                        <Text style={styles.actionSubtext}>Get instant solutions</Text>
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.actionCard} onPress={pickDocument}>
                        <View style={[styles.iconBox, { backgroundColor: 'rgba(139, 92, 246, 0.2)' }]}>
                            <FileText size={32} color={COLORS.secondary} />
                        </View>
                        <Text style={styles.actionText}>Upload PDF</Text>
                        <Text style={styles.actionSubtext}>Summarize & Solve</Text>
                    </TouchableOpacity>
                </View>

                <View style={styles.promoCard}>
                    <Text style={styles.promoTitle}>Unlock Limitless Learning</Text>
                    <Text style={styles.promoText}>Get unlimited scans and detailed explanations for just 1 JOD/month.</Text>
                    <GradientButton
                        title="Upgrade Now"
                        onPress={() => navigation.navigate('Subscription')}
                        style={{ marginTop: 16 }}
                    />
                </View>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: COLORS.background,
    },
    header: {
        padding: SPACING.l,
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    greeting: {
        color: COLORS.textSecondary,
        fontSize: 16,
    },
    appName: {
        color: COLORS.text,
        fontSize: 28,
        fontWeight: 'bold',
    },
    premiumBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(255, 215, 0, 0.15)',
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: 'rgba(255, 215, 0, 0.3)',
    },
    premiumText: {
        color: '#FFD700',
        fontWeight: 'bold',
        marginLeft: 6,
    },
    content: {
        padding: SPACING.l,
    },
    statsCard: {
        backgroundColor: COLORS.surface,
        borderRadius: 20,
        padding: SPACING.l,
        marginBottom: SPACING.xl,
        borderWidth: 1,
        borderColor: COLORS.surfaceLight,
    },
    statsTitle: {
        color: COLORS.textSecondary,
        marginBottom: SPACING.xs,
    },
    statsCount: {
        color: COLORS.text,
        fontSize: 32,
        fontWeight: 'bold',
        marginBottom: SPACING.m,
    },
    progressBarBg: {
        height: 8,
        backgroundColor: COLORS.surfaceLight,
        borderRadius: 4,
        marginBottom: SPACING.s,
        overflow: 'hidden',
    },
    progressBarFill: {
        height: '100%',
        backgroundColor: COLORS.primary,
        borderRadius: 4,
    },
    resetText: {
        color: COLORS.textSecondary,
        fontSize: 12,
    },
    sectionTitle: {
        color: COLORS.text,
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: SPACING.m,
    },
    grid: {
        flexDirection: 'row',
        gap: SPACING.m,
        marginBottom: SPACING.xl,
    },
    actionCard: {
        flex: 1,
        backgroundColor: COLORS.surface,
        borderRadius: 20,
        padding: SPACING.m,
        alignItems: 'center',
        borderWidth: 1,
        borderColor: COLORS.surfaceLight,
    },
    iconBox: {
        width: 64,
        height: 64,
        borderRadius: 32,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: SPACING.m,
    },
    actionText: {
        color: COLORS.text,
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 4,
        textAlign: 'center',
    },
    actionSubtext: {
        color: COLORS.textSecondary,
        fontSize: 12,
        textAlign: 'center',
    },
    promoCard: {
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderRadius: 20,
        padding: SPACING.l,
        borderWidth: 1,
        borderColor: 'rgba(16, 185, 129, 0.3)',
    },
    promoTitle: {
        color: COLORS.success,
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: SPACING.s,
    },
    promoText: {
        color: COLORS.textSecondary,
        marginBottom: SPACING.s,
        lineHeight: 20,
    },
});
